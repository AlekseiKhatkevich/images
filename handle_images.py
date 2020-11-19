from pathlib import Path
from typing import Container

from PIL import Image, ImageDraw, ImageFont


class AddSignature:
    """
    Добавляет подпись в изображения сохраняя их в отдельную папку.
    """
    font_size = 30
    title_font = ImageFont.truetype('fonts/PlayfairDisplay-Regular.ttf', font_size)
    title_text = 'Aleksei Khatkevich'
    color = (237, 230, 211)

    @staticmethod
    def get_files(source_folder: Path,
                  extensions: Container[str],
                  ) -> set:
        """
        Отдает сет с путями к файлам.
        extensions - список расширений файлов. Только файлы с данными расширениями будут найдены.
        """
        files_path = set()
        for file_path in source_folder.iterdir():
            if file_path.suffix[1:] in extensions:
                files_path.add(file_path)

        return files_path

    @classmethod
    def add_text(cls, file_path: Path, output_folder: Path) -> None:
        """
        Добавляет подпись в изображение и сохраняет его в  'output_folder'.
        """
        with Image.open(file_path) as image:
            image_w, image_h = image.size
            image_editable = ImageDraw.Draw(image)
            text_w, text_h = image_editable.textsize(cls.title_text, cls.title_font)

            x_pos = image_w - text_w - 10
            y_pos = image_h - text_h - 10

            image_editable.text(
                (x_pos, y_pos),
                cls.title_text,
                cls.color,
                font=cls.title_font,
            )

            image.save(output_folder / file_path.name)

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
        for file in files:
            self.add_text(file, output_folder)

