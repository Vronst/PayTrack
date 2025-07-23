"""All schemas in one place."""

from .category import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
)
from .currency import (
    CurrencyCreateSchema,
    CurrencyReadSchema,
    CurrencyUpdateSchema,
)
from .language import (
    LanguageCreateSchema,
    LanguageReadSchema,
    LanguageUpdateSchema,
)
from .receiver import (
    ReceiverCreateSchema,
    ReceiverReadSchema,
    ReceiverUpdateSchema,
)
from .savings import (
    SavingsCreateSchema,
    SavingsReadSchema,
    SavingsUpdateSchema,
)
from .setting import (
    SettingCreateSchema,
    SettingReadSchema,
    SettingUpdateSchema,
)
from .subscription import (
    SubscriptionCreateSchema,
    SubscriptionReadSchema,
    SubscriptionUpdateSchema,
)
from .subscription_share import (
    SubscriptionShareCreateSchema,
    SubscriptionShareReadSchema,
    SubscriptionShareUpdateSchema,
)
from .transaction import (
    TransactionCreateSchema,
    TransactionReadSchema,
    TransactionUpdateSchema,
)
from .transaction_share import (
    TransactionShareCreateSchema,
    TransactionShareReadSchema,
    TransactionShareUpdateSchema,
)
from .translation import (
    TranslationCreateSchema,
    TranslationReadSchema,
    TranslationUpdateSchema,
)
from .user import UserCreateSchema, UserReadSchema, UserUpdateSchema

__all__ = [
    "CategoryReadSchema",
    "CategoryCreateSchema",
    "CategoryUpdateSchema",
    "CurrencyReadSchema",
    "CurrencyCreateSchema",
    "CurrencyUpdateSchema",
    "LanguageReadSchema",
    "LanguageUpdateSchema",
    "LanguageCreateSchema",
    "ReceiverReadSchema",
    "ReceiverCreateSchema",
    "ReceiverUpdateSchema",
    "SavingsReadSchema",
    "SavingsCreateSchema",
    "SavingsUpdateSchema",
    "SettingReadSchema",
    "SettingUpdateSchema",
    "SettingCreateSchema",
    "SubscriptionReadSchema",
    "SubscriptionCreateSchema",
    "SubscriptionUpdateSchema",
    "SubscriptionShareReadSchema",
    "SubscriptionShareCreateSchema",
    "SubscriptionShareUpdateSchema",
    "TranslationReadSchema",
    "TranslationCreateSchema",
    "TranslationUpdateSchema",
    "TransactionCreateSchema",
    "TransactionUpdateSchema",
    "TransactionReadSchema",
    "UserReadSchema",
    "UserCreateSchema",
    "UserUpdateSchema",
    "TransactionShareCreateSchema",
    "TransactionShareReadSchema",
    "TransactionShareUpdateSchema",
]
