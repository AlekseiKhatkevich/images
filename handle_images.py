import argparse
from pathlib import Path
from typing import Container

from PIL import Image, ImageDraw, ImageFont


class AddSignature:
    """
    Добавляет подпись в изображения сохраняя их в отдельную папку.
    """
    def __init__(self,
                 title_font: str = 'fonts/PlayfairDisplay-Regular.ttf',
                 title_text: str = 'Aleksei Khatkevich',
                 color: tuple = (237, 230, 211),
                 source_folder: str = 'source-images',
                 output_folder: str = 'output-images',
                 extensions: Container[str] = ('jpg',),
                 max_font_size: int = 50,
                 ) -> None:
        """
        :param title_font: размер шрифта
        :param title_text: текст добавляемый на изображение
        :param color: цвет текста
        :param source_folder: папка с исходными изображениями
        :param output_folder: папка с подписанными изображениями
        :param extensions: допустимые расширения файлов
        :param max_font_size: максимальный размер шрифта
        """
        self.title_font = title_font
        self.title_text = title_text
        self.color = color
        self.source_folder = Path(source_folder)
        self.output_folder = Path(output_folder)
        self.extensions = extensions
        self.max_font_size = max_font_size

    def get_files(self, source_folder: Path) -> set:
        """
        Отдает сет с путями к файлам.
        """
        files_path = set()
        for file_path in source_folder.iterdir():
            if file_path.suffix[1:] in self.extensions:
                files_path.add(file_path)

        return files_path

    def add_text(self, file_path: Path) -> None:
        """
        Добавляет подпись в изображение и сохраняет его в 'output_folder'.
        """
        with Image.open(file_path) as image:
            # Линейные размеры изображения
            image_w, image_h = image.size
            image_editable = ImageDraw.Draw(image)
            # Размер шрифта зависит от размеров изображения, но не более "max_font_size"
            font_size = min(
                self.max_font_size,
                int((image_w * image_h) / 19000),
            )
            title_font = ImageFont.truetype(self.title_font, font_size)
            # Линейные размеры текста.
            text_w, text_h = image_editable.textsize(self.title_text, title_font)
            # Координаты расположения текста
            x_pos = (image_w - text_w) * 0.98
            y_pos = (image_h - text_h) * 0.98

            image_editable.text(
                (x_pos, y_pos),
                self.title_text,
                self.color,
                font=title_font,
            )

            image.save(self.output_folder / file_path.name)

    def __call__(self) -> None:
        """
        Запускает весь процесс:
        1) Создаем папку "output_folder" если нужно.
        2) Получаем список файлов.
        3) Создаем новые файлы с подписями и сохраняем их.
        """

        Path(self.output_folder).mkdir(parents=True, exist_ok=True)

        files_path = self.get_files(self.source_folder)
        for path in files_path:
            self.add_text(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Выбор возможного пути сохранения подписанных изображений.',
    )
    parser.add_argument(
        '--path',
        metavar='--path',
        type=str,
        help='Альтернативный путь сохранения подписанных изображений',
        default=Path('output-images')
    )
    args = parser.parse_args()

    AddSignature(output_folder=args.path)()