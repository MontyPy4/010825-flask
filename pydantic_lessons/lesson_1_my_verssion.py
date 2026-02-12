from pydantic import BaseModel
from pydantic import Field
from pydantic import BaseModel
# from pydantic import Field, field_validator, model_validator, BaseModel
#
# class Address(BaseModel):
#     city: str
#     street: str
#     post_code: str
#
#
# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#     is_active: bool
#     address: Address
#
#
# address = Address(
#     city="Warsaw",
#     street="Main Street",
#     post_code="X0-73"
# )
#
# user = User(
#     id=1,
#     name="123123",
#     age=40,
#     is_active=True,
#     address=address
# )
#
#
# print(user)
#
# User.model_validate_json(json_data)
#
# class Address(BaseModel):
#     city: str
#     street: str
#     house_number: int
#
#
# class User(BaseModel):
#     name: str
#     age: int
#     email: str
#     address: Address
#
#
# json_data = """{
#     "name": "Dmitry",
#     "age": 26,
#     "email": "qwerty",
#     "address": {
#         "city": "Berlin",
#         "street": "Test street",
#         "house_number": "123"
#     }
# }"""
#
#
# user = User.model_validate_json(json_data)
#
# print(user)
#
#
# from enum import StrEnum
# from datetime import datetime
# import re
#
# class TestType(StrEnum):
#     BLOOD = "blood"
#     URINE = "urine"
#     XRAY = "Xray"
#     MRI = "mri"
#
#
# class LabTestBase(BaseModel):
#     patient_id: int
#     test_type: TestType
#     test_date: datetime
#
#
# class LabTestRequest(LabTestBase):
#     notes: str
#
#
# class LabTestResponse(LabTestBase):
#     id: int
#     result: str
#     is_completed: bool
#
#
# class LabTestResponse(LabTestBase):
#     id: int
#     result: str | None = None
#     is_completed: bool
#
#     def is_urgent(self) -> bool:
#         if not self.result:
#             return False
#
#         if "гемоглобин" in self.result.lower():
#             match_pattern = re.search(r"(\d+)\s*г/л", self.result.lower())
#             if match_pattern:
#                 value = int(match_pattern.group(1))
#                 return value < 90 or value > 160  # value == 85 -> CRITICAL | value == 170 -> CRITICAL
#         return False
#
# raw_data = """{
#     "id": 1,
#     "patient_id": 123,
#     "test_type": "blood",
#     "test_date": "2025-01-12T14:58:33",
#     "result": "Гемоглобин: 200 г/л",
#     "is_completed": true
# }"""
#
# class TestData(BaseUser):
#     test: str = Field(min_length=2, max_length=25)
#     test1: str = Field(min_length=2, max_length=25)
#     test2: str = Field(min_length=2, max_length=25)
#     test3: str = Field(min_length=2, max_length=25)
#
#
# data = {
#     "test": input(),
#     "test1": input(),
#     "test2": input(),
#     "test3": input(),
# }