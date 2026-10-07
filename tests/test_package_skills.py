import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "package_skills", ROOT / "scripts" / "package_skills.py"
)
package_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package_skills)


def write_skill(root: Path, directory: str, name: str, description: str, body: str = "") -> Path:
    skill_dir = root / "skills" / directory
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n{body}",
        encoding="utf-8",
    )
    return skill_dir


class SkillDiscoveryTests(unittest.TestCase):
    def test_discovery_reads_sorted_names_and_descriptions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root, "zeta", "zeta", "Last description")
            write_skill(root, "alpha", "alpha", "First description")

            self.assertEqual(
                package_skills.discover_skills(root / "skills"),
                [
                    {"name": "alpha", "description": "First description"},
                    {"name": "zeta", "description": "Last description"},
                ],
            )

    def test_discovery_rejects_invalid_directory_or_metadata_name(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root, "wrong-directory", "other-name", "Description")

            with self.assertRaisesRegex(ValueError, "name"):
                package_skills.discover_skills(root / "skills")

    def test_discovery_rejects_invalid_name_syntax(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root, "bad name", "bad name", "Description")

            with self.assertRaisesRegex(ValueError, "name"):
                package_skills.discover_skills(root / "skills")

    def test_discovery_rejects_manifest_symlink_outside_skills_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            skill = write_skill(root, "alpha", "alpha", "Description")
            outside = Path(temporary) / "outside.md"
            outside.write_text(
                "---\nname: alpha\ndescription: Outside metadata\n---\n", encoding="utf-8"
            )
            (skill / "SKILL.md").unlink()
            (skill / "SKILL.md").symlink_to(outside)

            with self.assertRaisesRegex(ValueError, "outside|symlink|manifest"):
                package_skills.discover_skills(root / "skills")

class DependencyCollectionTests(unittest.TestCase):
    def test_collects_transitive_markdown_dependencies_once(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = write_skill(
                root,
                "alpha",
                "alpha",
                "Description",
                "See [policy](../../shared/a.md#section).",
            )
            shared = root / "shared"
            templates = root / "templates"
            shared.mkdir()
            templates.mkdir()
            (shared / "a.md").write_text(
                "See [template](../templates/form.md) and [policy](b.md).",
                encoding="utf-8",
            )
            (shared / "b.md").write_text("End.", encoding="utf-8")
            venues = root / "venues"
            venues.mkdir()
            (templates / "form.md").write_text(
                "Blank form; see [venue guide](../venues/README.md).", encoding="utf-8"
            )
            (venues / "README.md").write_text("Current-source guidance.", encoding="utf-8")
            (shared / "unused.md").write_text("Unused.", encoding="utf-8")

            resources = package_skills.collect_dependencies(root, skill)

            self.assertEqual(
                {path.relative_to(root).as_posix() for path in resources},
                {
                    "skills/alpha/SKILL.md",
                    "shared/a.md",
                    "shared/b.md",
                    "templates/form.md",
                    "venues/README.md",
                },
            )

    def test_external_and_anchor_only_links_add_no_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = write_skill(
                root,
                "alpha",
                "alpha",
                "Description",
                "[web](https://example.org/paper) [section](#workflow).",
            )

            self.assertEqual(
                package_skills.collect_dependencies(root, skill),
                [skill / "SKILL.md"],
            )

    def test_broken_local_link_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = write_skill(root, "alpha", "alpha", "Description", "[missing](missing.md)")

            with self.assertRaisesRegex(ValueError, "missing|Missing|unresolved|Unresolved"):
                package_skills.collect_dependencies(root, skill)

    def test_unsupported_local_resource_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = write_skill(root, "alpha", "alpha", "Description", "[image](plot.png)")
            (skill / "plot.png").write_bytes(b"image")

            with self.assertRaisesRegex(ValueError, "unsupported|Unsupported"):
                package_skills.collect_dependencies(root, skill)

    def test_local_image_with_unsupported_resource_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = write_skill(root, "alpha", "alpha", "Description", "![plot](plot.png)")
            (skill / "plot.png").write_bytes(b"image")

            with self.assertRaisesRegex(ValueError, "unsupported|Unsupported"):
                package_skills.collect_dependencies(root, skill)

    def test_fenced_code_links_are_not_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = write_skill(
                root,
                "alpha",
                "alpha",
                "Description",
                "```markdown\n[example](../../shared/not-a-real-file.md)\n```\n",
            )

            self.assertEqual(package_skills.collect_dependencies(root, skill), [skill / "SKILL.md"])

    def test_link_outside_repository_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            skill = write_skill(root, "alpha", "alpha", "Description", "[escape](../../../escape.md)")

            with self.assertRaisesRegex(ValueError, "outside|Outside|escape|Escape"):
                package_skills.collect_dependencies(root, skill)

    def test_symlink_outside_repository_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            skill = write_skill(root, "alpha", "alpha", "Description", "[escape](leak.md)")
            outside = Path(temporary) / "outside.md"
            outside.write_text("Private content is test-only.", encoding="utf-8")
            try:
                (skill / "leak.md").symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks are unavailable")

            with self.assertRaisesRegex(ValueError, "outside|Outside|escape|Escape"):
                package_skills.collect_dependencies(root, skill)


def make_package_fixture(root: Path) -> Path:
    skill = write_skill(
        root,
        "alpha",
        "alpha",
        "Description",
        "Read [policy][policy-ref], [guide](../../shared/name%20with%20space.md), "
        "[external](https://example.org), and [workflow](#workflow).\n\n"
        "[policy-ref]: ../../shared/policy.md#scope\n\n"
        "```markdown\n[example](../../shared/not-a-real-file.md)\n```\n",
    )
    (root / "shared").mkdir()
    (root / "templates").mkdir()
    (root / "venues").mkdir()
    (root / "shared" / "policy.md").write_text(
        "See [form](../templates/form.md).", encoding="utf-8"
    )
    (root / "shared" / "name with space.md").write_text("A spaced file.", encoding="utf-8")
    (root / "templates" / "form.md").write_text(
        "See [venue guide](../venues/README.md).", encoding="utf-8"
    )
    (root / "venues" / "README.md").write_text("Official-source reminder.", encoding="utf-8")
    (root / "shared" / "unused.md").write_text("Unused resource.", encoding="utf-8")
    (root / "LICENSE").write_text("Synthetic test license notice.", encoding="utf-8")
    return skill


class BundleGenerationTests(unittest.TestCase):
    def test_builds_self_contained_bundle_and_rewrites_recursive_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            make_package_fixture(root)
            output = Path(temporary) / "dist"

            bundle = package_skills.build_bundle(root, "alpha", output)

            self.assertEqual(bundle, output / "skills" / "alpha")
            self.assertEqual(list(bundle.rglob("SKILL.md")), [bundle / "SKILL.md"])
            self.assertEqual(package_skills.validate_bundle(bundle), [])
            skill_text = (bundle / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(skill_text.startswith("---\nname: alpha\ndescription: Description\n---"))
            self.assertIn("[external](https://example.org)", skill_text)
            self.assertIn("[workflow](#workflow)", skill_text)
            self.assertIn("[policy][policy-ref]", skill_text)
            self.assertIn("[policy-ref]: references/shared/policy.md#scope", skill_text)
            self.assertIn("[policy][policy-ref]", skill_text)
            self.assertIn(
                "[guide](references/shared/name%20with%20space.md)", skill_text
            )
            self.assertIn("[example](../../shared/not-a-real-file.md)", skill_text)
            self.assertEqual((bundle / "LICENSE").read_text(encoding="utf-8"), "Synthetic test license notice.")
            self.assertIn(
                "[form](../templates/form.md)",
                (bundle / "references" / "shared" / "policy.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "[venue guide](../venues/README.md)",
                (bundle / "references" / "templates" / "form.md").read_text(encoding="utf-8"),
            )
            self.assertTrue((bundle / "references" / "venues" / "README.md").is_file())
            self.assertFalse((bundle / "references" / "shared" / "unused.md").exists())

    def test_bundle_generation_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            make_package_fixture(root)
            output = Path(temporary) / "dist"
            destination = output / "skills" / "alpha"
            destination.mkdir(parents=True)
            marker = destination / "keep.txt"
            marker.write_text("preserve", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "exist|collision|already"):
                package_skills.build_bundle(root, "alpha", output)
            self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")

    def test_validation_rejects_invalid_metadata_and_broken_local_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "alpha"
            bundle.mkdir()
            (bundle / "SKILL.md").write_text(
                "---\nname: wrong name\ndescription: Description\n---\n\n[missing](missing.md)",
                encoding="utf-8",
            )

            errors = package_skills.validate_bundle(bundle)

            self.assertTrue(any("name" in error.lower() for error in errors))
            self.assertTrue(any("missing" in error.lower() or "broken" in error.lower() for error in errors))

    def test_validation_requires_exactly_one_skill_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "alpha"
            nested = bundle / "references"
            nested.mkdir(parents=True)
            valid = "---\nname: alpha\ndescription: Description\n---\n"
            (bundle / "SKILL.md").write_text(valid, encoding="utf-8")
            (nested / "SKILL.md").write_text(valid, encoding="utf-8")

            errors = package_skills.validate_bundle(bundle)

            self.assertTrue(any("exactly one" in error.lower() for error in errors))

    def test_validation_rejects_malformed_or_out_of_spec_frontmatter(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "alpha"
            bundle.mkdir()
            (bundle / "SKILL.md").write_text(
                "---\nname: alpha\ndescription: {mapping: invalid}\n---\n", encoding="utf-8"
            )

            errors = package_skills.validate_bundle(bundle)

            self.assertTrue(any("description" in error.lower() or "scalar" in error.lower() for error in errors))

    def test_validation_rejects_unterminated_quoted_frontmatter(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "alpha"
            bundle.mkdir()
            (bundle / "SKILL.md").write_text(
                '---\nname: alpha\ndescription: "unterminated\n---\n', encoding="utf-8"
            )

            errors = package_skills.validate_bundle(bundle)

            self.assertTrue(any("malformed" in error.lower() for error in errors))

    def test_validation_enforces_name_and_description_lengths(self):
        with tempfile.TemporaryDirectory() as temporary:
            long_name = "a" * 65
            bundle = Path(temporary) / long_name
            bundle.mkdir()
            description = "d" * 1025
            (bundle / "SKILL.md").write_text(
                f"---\nname: {long_name}\ndescription: {description}\n---\n", encoding="utf-8"
            )

            errors = package_skills.validate_bundle(bundle)

            self.assertTrue(any("name" in error.lower() for error in errors))
            self.assertTrue(any("description" in error.lower() for error in errors))

    def test_validation_does_not_read_symlinked_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "alpha"
            bundle.mkdir()
            outside = Path(temporary) / "outside.md"
            outside.write_text(
                "---\nname: wrong\ndescription: Outside file\n---\n", encoding="utf-8"
            )
            (bundle / "SKILL.md").symlink_to(outside)

            errors = package_skills.validate_bundle(bundle)

            self.assertEqual(len(errors), 1)
            self.assertIn("symlink", errors[0].lower())

    def test_zip_has_one_skill_directory_at_archive_root(self):
        import zipfile

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            make_package_fixture(root)
            output = Path(temporary) / "dist"
            bundle = package_skills.build_bundle(root, "alpha", output)
            archive = output / "zips" / "alpha.zip"

            result = package_skills.create_zip(bundle, archive)

            self.assertEqual(result, archive)
            with zipfile.ZipFile(archive) as zipped:
                names = zipped.namelist()
                self.assertTrue(names)
                self.assertEqual({name.split("/", 1)[0] for name in names}, {"alpha"})
                extracted = Path(temporary) / "extracted"
                zipped.extractall(extracted)
            self.assertEqual(package_skills.validate_bundle(extracted / "alpha"), [])

    def test_zip_ignores_preexisting_predictable_temporary_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            make_package_fixture(root)
            bundle = package_skills.build_bundle(root, "alpha", Path(temporary) / "dist")
            zip_dir = Path(temporary) / "zips"
            zip_dir.mkdir()
            archive = zip_dir / "alpha.zip"
            outside = Path(temporary) / "outside.txt"
            outside.write_text("preserve", encoding="utf-8")
            (zip_dir / ".alpha.zip.tmp").symlink_to(outside)

            package_skills.create_zip(bundle, archive)

            self.assertEqual(outside.read_text(encoding="utf-8"), "preserve")
            self.assertTrue(archive.is_file())

    def test_bundle_output_rejects_symlinked_skills_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            make_package_fixture(root)
            output = Path(temporary) / "dist"
            output.mkdir()
            outside = Path(temporary) / "outside"
            outside.mkdir()
            (output / "skills").symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "outside|symlink|output"):
                package_skills.build_bundle(root, "alpha", output)
            self.assertEqual(list(outside.iterdir()), [])


class InstallationAndCliTests(unittest.TestCase):
    def make_bundle(self, temporary: str) -> tuple[Path, Path]:
        root = Path(temporary) / "repo"
        root.mkdir()
        make_package_fixture(root)
        bundle = package_skills.build_bundle(root, "alpha", Path(temporary) / "dist")
        return root, bundle

    def test_installs_directory_bundle_into_explicit_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, bundle = self.make_bundle(temporary)
            destination = Path(temporary) / "project" / ".agents" / "skills"

            installed = package_skills.install_bundle(bundle, destination)

            self.assertEqual(installed, destination / "alpha")
            self.assertEqual(package_skills.validate_bundle(installed), [])

    def test_installs_zip_bundle_into_explicit_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, bundle = self.make_bundle(temporary)
            archive = Path(temporary) / "alpha.zip"
            package_skills.create_zip(bundle, archive)
            destination = Path(temporary) / "user" / "skills"

            installed = package_skills.install_bundle(archive, destination)

            self.assertEqual(installed, destination / "alpha")
            self.assertEqual(package_skills.validate_bundle(installed), [])

    def test_install_collision_preserves_existing_files_unless_replace_is_explicit(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, bundle = self.make_bundle(temporary)
            destination = Path(temporary) / "skills"
            existing = destination / "alpha"
            existing.mkdir(parents=True)
            (existing / "user-file.txt").write_text("keep", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "exist|collision|already"):
                package_skills.install_bundle(bundle, destination)
            self.assertEqual((existing / "user-file.txt").read_text(encoding="utf-8"), "keep")

            installed = package_skills.install_bundle(bundle, destination, replace=True)

            self.assertEqual(installed, existing)
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertFalse((installed / "user-file.txt").exists())

    def test_replace_removes_destination_symlink_without_touching_its_target(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, bundle = self.make_bundle(temporary)
            destination = Path(temporary) / "skills"
            destination.mkdir()
            outside = Path(temporary) / "outside"
            outside.mkdir()
            marker = outside / "preserve.txt"
            marker.write_text("keep", encoding="utf-8")
            (destination / "alpha").symlink_to(outside, target_is_directory=True)

            installed = package_skills.install_bundle(bundle, destination, replace=True)

            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_cli_package_rejects_symlinked_zip_directory_outside_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "dist"
            output.mkdir()
            outside = Path(temporary) / "outside"
            outside.mkdir()
            (output / "zips").symlink_to(outside, target_is_directory=True)

            status = package_skills.main(
                ["package", "--skill", "citation-verifier", "--output", str(output), "--zip"]
            )

            self.assertEqual(status, 1)
            self.assertEqual(list(outside.iterdir()), [])

    def test_install_rejects_invalid_bundle_before_creating_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            invalid = Path(temporary) / "invalid"
            invalid.mkdir()
            (invalid / "SKILL.md").write_text("not frontmatter", encoding="utf-8")
            destination = Path(temporary) / "skills"

            with self.assertRaisesRegex(ValueError, "invalid|frontmatter|manifest"):
                package_skills.install_bundle(invalid, destination)
            self.assertFalse(destination.exists())

    def test_zip_install_rejects_traversal_member(self):
        import zipfile

        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "unsafe.zip"
            with zipfile.ZipFile(archive, "w") as zipped:
                zipped.writestr("alpha/SKILL.md", "---\nname: alpha\ndescription: Safe\n---\n")
                zipped.writestr("../escaped.md", "outside")
            destination = Path(temporary) / "skills"

            with self.assertRaisesRegex(ValueError, "unsafe|traversal|path|member"):
                package_skills.install_bundle(archive, destination)
            self.assertFalse((Path(temporary) / "escaped.md").exists())
            self.assertFalse(destination.exists())

    def test_zip_install_rejects_symlink_member(self):
        import stat
        import zipfile

        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "unsafe.zip"
            with zipfile.ZipFile(archive, "w") as zipped:
                zipped.writestr("alpha/SKILL.md", "---\nname: alpha\ndescription: Safe\n---\n")
                link = zipfile.ZipInfo("alpha/link.md")
                link.create_system = 3
                link.external_attr = (stat.S_IFLNK | 0o777) << 16
                zipped.writestr(link, "../../outside.md")
            destination = Path(temporary) / "skills"

            with self.assertRaisesRegex(ValueError, "symlink|unsafe|member"):
                package_skills.install_bundle(archive, destination)
            self.assertFalse(destination.exists())

    def test_cli_lists_packages_validates_and_installs(self):
        from contextlib import redirect_stderr, redirect_stdout

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "dist"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                list_status = package_skills.main(["list", "--path", str(ROOT / "skills")])
                package_status = package_skills.main(
                    ["package", "--skill", "citation-verifier", "--output", str(output), "--zip"]
                )
                validate_status = package_skills.main(
                    ["validate", str(output / "skills" / "citation-verifier")]
                )
                install_status = package_skills.main(
                    [
                        "install",
                        str(output / "zips" / "citation-verifier.zip"),
                        "--destination",
                        str(Path(temporary) / "installed"),
                    ]
                )

            self.assertEqual((list_status, package_status, validate_status, install_status), (0, 0, 0, 0))
            self.assertIn("citation-verifier", stdout.getvalue())
            self.assertEqual(stderr.getvalue(), "")
            self.assertTrue(
                (Path(temporary) / "installed" / "citation-verifier" / "SKILL.md").is_file()
            )


if __name__ == "__main__":
    unittest.main()
