from src.utils import storage
import json, pytest

SAMPLE_DATA = {
	"key1": "value1",
	"key2": "value2"
}
PASSWORD = b"master_password123"

class TestWriteJSON:
	"""Unit tests for 'storage.write_json'."""

	def test_write_plain(self, tmp_path):
		"""Verify 'storage.write_json' correctly writes plain text."""
		test_file = tmp_path / "test.json"
		storage.write_json(
			contents=SAMPLE_DATA,
			file=test_file,
			encrypt=False
		)

		assert test_file.exists()

		with open(test_file, "rt") as f:
			data = json.load(f)
		assert data == SAMPLE_DATA

	def test_write_encrypted(self, tmp_path):
		"""Verify 'storage.write_json' correctly writes encrypted content."""
		test_file = tmp_path / "test.json"
		storage.write_json(
			contents=SAMPLE_DATA,
			file=test_file,
			encrypt=True,
			master_password=PASSWORD
		)

		assert test_file.exists()

		contents = test_file.read_text()
		assert "key1" not in contents
		assert ":" in contents	# Salt and content separator (<salt>:<encrypted content>).

	def test_raise_value_error(self, tmp_path):
		"""Verify 'storage.write_json' raises ValueError is 'encrypt == True'
		and 'master_password' is not given."""
		test_file = tmp_path / "test.json"

		with pytest.raises(ValueError):
			storage.write_json(
				contents=SAMPLE_DATA,
				file=test_file,
				encrypt=True
			)

class TestReadJSON:
	"""Unit tests for 'storage.read_json'."""

	def test_read_plain(self, tmp_path):
		"""
		Verify 'storage.read_json' correctly reads plain text
		json files.
		"""
		test_file = tmp_path / "test.json"
		test_file.write_text(
			json.dumps(SAMPLE_DATA)
		)

		contents = storage.read_json(
			file=test_file,
			encrypted=False
		)
		assert contents == SAMPLE_DATA

	def test_read_encrypted(self, tmp_path):
		"""
		Verify 'storage.read_json' correctly reads encrypted
		json files.
		"""
		test_file = tmp_path / "test.json"
		storage.write_json(
			contents=SAMPLE_DATA,
			file=test_file,
			encrypt=True,
			master_password=PASSWORD
		)

		contents = storage.read_json(
			file=test_file,
			encrypted=True,
			master_password=PASSWORD
		)
		assert contents == SAMPLE_DATA

	def test_raise_value_error(self, tmp_path):
		"""
		Verify 'storage.read_json' raises ValueError when
		'encrypted == True' and 'master_password' is not
		provided.
		"""
		test_file = tmp_path / "test.json"
		test_file.write_text(
			json.dumps(SAMPLE_DATA)
		)

		with pytest.raises(ValueError):
			storage.read_json(
				file=test_file,
				encrypted=True
			)