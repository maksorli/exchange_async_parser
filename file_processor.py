import pandas as pd
from utils import setup_logger

logger = setup_logger("FileProcessor", "logs.log")


class FileProcessor:
    def __init__(self, file_content):
        self.file_content = file_content

    def read_and_process(self):
        try:
            logger.info("Начало обработки файла.")
            df = pd.read_excel(self.file_content, engine="xlrd")
            df.columns = [
                "1",
                "exchange_product_id",
                "exchange_product_name",
                "delivery_basis_name",
                "volume",
                "total",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "count",
            ]

            metric_ton_row = df[
                df.apply(
                    lambda x: x.astype(str)
                    .str.contains("Единица измерения: Метрическая тонна")
                    .any(),
                    axis=1,
                )
            ]

            if metric_ton_row.empty:
                logger.warning(
                    "Строка с 'Единица измерения: Метрическая тонна' не найдена."
                )
                return None

            metric_ton_index = metric_ton_row.index[0]
            start_index = metric_ton_index + 3
            # logger.info(f"Таблица начинается со строки  {metric_ton_index+3}")

            rows = []
            for index, row in df.iloc[start_index:].iterrows():
                if row.astype(str).str.contains("Итого:", case=False).any():
                    # logger.info(f"'Итого' найдено на строке с индексом {index}")
                    break
                try:
                    if int(row["count"]) > 0:
                        rows.append(row)
                except (ValueError, TypeError):
                    pass

            return pd.DataFrame(rows)

        except Exception as e:
            logger.error(f"Ошибка при обработке файла: {e}")
            return None
