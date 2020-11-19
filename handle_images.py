from pathlib import Path
from typing import Container, Generator


class AddSignature:
    """
    Добавляет подпись в изображения сохраняя их в отдельную папку.
    """
    @staticmethod
    def get_files(source_folder: Path,
                  extensions: Container[str],
                  ) -> set:
        """

        """
        files = set()
        for file in source_folder.glob('*'):
            if file.suffix[1:] in extensions:
                files.add(file)

        return files

    def __call__(self,
                 source_folder: str = 'source-images',
                 extensions: Container[str] = ('jpg',),
                 output_folder: str = 'output-images',
                 ) -> None:
        """
        """
        source_folder = Path(source_folder)
        output_folder = Path(output_folder)

        files = self.get_files(source_folder, extensions)

        return  files