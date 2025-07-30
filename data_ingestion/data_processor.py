import re
from typing import List
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

# @dataclass
# class Phone:
#     file_path : str
#
#     def importing(self) -> list|None:
#         try:
#             with open(self.file_path, 'r') as f:
#                 datas: list = f.readlines()
#                 logger.info("Data extraction successfully")
#                 return datas
#         except Exception as e:
#             logger.exception(f"Exception error: {e}")
#
#     def preprocessing(self, datas):
#         pattern = "^[\+0-9]+[-0-9]+$"







# file = "text.txt"
# # phone: list = []
#
# try:
#     with open(file,"r") as f:
#         phone_num = f.readlines()
#         logger.info("File read successfully")
# except Exception as e:
#     logger.error(f"Error {e}")
#
# logger.info(phone_num)



        # pattern = "^[\+0-9]+[-0-9]+$"
        # if re.match(pattern, f)

# books_raw: List[Dict[str, Any]] = json.load(f)
datas = ['+977-9810589705', '+91-740-63-99757', '4935812398', '+1-568-845-54565']
print(datas)
for data in datas:
    data = re.sub(r'\D','',data)
    if data.startswith("00"):
        data = data[2:]
    if data.startswith("+"):
        data = data[1:]
    if len(data)>10:
        country_code = data[:-10]
        national_number = data[-10:]
    else:
        country_code = 91
        national_number = data.zfill(10)
    formatted = f"+{country_code}-{national_number[:3]}-{national_number[3:6]}-{national_number[6:10]}"
    print(formatted)

    # pattern = "^[+0-9]+[-0-9]+$"
    # pattern_needed = "^[+0-9]+[-0-9]+$"
    # data_after = re.sub(pattern, pattern_needed, data)
    # print(data_after)