# noqa: D100

#
# class TestPositiveUser:  # noqa: D101
#     def test_name_validation_special(self, session):  # noqa: D102
#         name: str = "test@ser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "123456"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#             pin=pin,
#         )
#
#         session.add(user)
#         session.commit()
#
#         assert user.name == name
#
#     def test_name_validation_digits(self, session):  # noqa: D102
#         name: str = "test2se1"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "123456"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#             pin=pin,
#         )
#
#         session.add(user)
#         session.commit()
#
#         assert user.name == name
#
#     def test_name_validation(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "123456"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#             pin=pin,
#         )
#
#         session.add(user)
#         session.commit()
#
#         assert user.name == name
#
#     def test_pin_validation(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "123456"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#             pin=pin,
#         )
#
#         session.add(user)
#         session.commit()
#
#         assert user.pin == pin
#
#     def test_phone_validation(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         phone: str = "999999999"
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#             phone=phone,
#         )
#
#         session.add(user)
#         session.commit()
#
#         assert user.phone == phone.replace(" ", "")
#
#     def test_phone_validation_with_prefix(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         phone: str = "+48999999999"
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#             phone=phone,
#         )
#
#         session.add(user)
#         session.commit()
#
#         assert user.phone == phone.replace(" ", "")
#
#     def test_phone_validation_with_spaces_and_prefix(self, session):
# noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         phone: str = "+48 999 999 999"
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#             phone=phone,
#         )
#
#         session.add(user)
#         session.commit()
#
#         assert user.phone == phone.replace(" ", "")
#
#     @pytest.mark.regression
#     def test_email_validation(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#         )
#
#         session.add(user)
#         session.commit()
#
#     @pytest.mark.regression
#     def test_email_validator_with_numbers(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test1@test2.com"
#         password: str = "testpass"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#         )
#
#         session.add(user)
#         session.commit()
#
#     @pytest.mark.regression
#     def test_creation_company_True(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         user: User = User(
#             name=name,
#             company=company,
#             email=email,
#             password=password,
#             pin=PIN_LENGTH * "1",
#         )
#
#         session.add(user)
#         session.commit()
#
#         assert user.name == name
#         assert user.surname is None
#         assert user.email == email
#         assert user.password == password
#         assert user.company == company
#         assert not user.premium
#         assert user.parent_id is None
#         assert user.parent is None
#         assert user.phone is None
#         assert user.included == []
#         assert user.subaccounts == []
#         assert user.settings is None
#         assert user.transactions == []
#         assert user.included_in_transactions == []
#         assert user.other_receivers == []
#         assert user.savings is None
#         assert user.subscriptions == []
#         assert user.subscription_shares == []
#         assert user.included_in_subscriptions == []
#         assert user.transactions_shares == []
#
#     @pytest.mark.regression
#     def test_creation_company_false(self, session):  # noqa: D102
#         name: str = "testuser"
#         surname: str = "testsurname"
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         user: User = User(
#             name=name,
#             surname=surname,
#             email=email,
#             password=password,
#             pin=PIN_LENGTH * "1",
#         )
#
#         session.add(user)
#         session.commit()
#
#         assert user.name == name
#         assert user.surname == surname
#         assert user.email == email
#         assert user.password == password
#         assert not user.company
#         assert not user.premium
#         assert user.parent_id is None
#         assert user.parent is None
#         assert user.phone is None
#         assert user.included == []
#         assert user.subaccounts == []
#         assert user.settings is None
#         assert user.transactions == []
#         assert user.included_in_transactions == []
#         assert user.other_receivers == []
#         assert user.savings is None
#         assert user.subscriptions == []
#         assert user.subscription_shares == []
#         assert user.included_in_subscriptions == []
#         assert user.transactions_shares == []
#
#
# class TestNegativeUser:  # noqa: D101
#     @pytest.mark.regression
#     def test_email_validator_no_dot(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@testcom"
#         password: str = "testpass"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#             )
#
#             session.add(user)
#             session.commit()
#
#     @pytest.mark.regression
#     def test_email_validator_no_end(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test"
#         password: str = "testpass"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#             )
#
#             session.add(user)
#             session.commit()
#
#     @pytest.mark.regression
#     def test_email_validator_no_at(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "testtest.com"
#         password: str = "testpass"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#             )
#
#             session.add(user)
#             session.commit()
#
#     @pytest.mark.regression
#     def test_email_validator_invalid_space(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test @test.com"
#         password: str = "testpass"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_phone_validation_wrong_prefix(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         phone: str = "+ 999999999"
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 phone=phone,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_phone_validation_empty(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         phone: str = ""
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 phone=phone,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_phone_validation_with_letters(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         phone: str = "9a9999999"
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 phone=phone,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_phone_validation_too_many_digits(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         phone: str = "9999999999"
#         email: str = "test@test.com"
#         password: str = "testpass"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 phone=phone,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_pin_validation_special_sign(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "1!9944"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 pin=pin,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_pin_validation_spaces(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "1 9944"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 pin=pin,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_pin_validation_letters(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "1a3b44"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 pin=pin,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_pin_validation_too_short(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "1" * 5
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 pin=pin,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_pin_validation_too_long(self, session):  # noqa: D102
#         name: str = "testuser"
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "1" * 7
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 pin=pin,
#             )
#
#             session.add(user)
#             session.commit()
#
#     def test_name_validation_too_long(self, session):  # noqa: D102
#         name: str = "t" * 31
#         company: bool = True
#         email: str = "test@test.com"
#         password: str = "testpass"
#         pin: str = "123456"
#
#         with pytest.raises(ValueError):
#             user: User = User(
#                 name=name,
#                 company=company,
#                 email=email,
#                 password=password,
#                 pin=pin,
#             )
#
#             session.add(user)
#             session.commit()
