class User:
    def __init__(self, id, **kwargs):
        """
        ساخت یک کاربر جدید. id اجباریه ولی بقیه اطلاعات مثل username، name و غیره دلخواهه.
        """
        self.id = id
        # این حلقه باعث میشه هر فیلد اضافه‌ای که پاس داده شد
        # به صورت خودکار به عنوان ویژگی‌های (attributes) این آبجکت ذخیره بشه
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        """
        تبدیل آبجکت کاربر به دیکشنری برای ذخیره در فایل JSON
        """
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        """
        ساخت آبجکت کاربر از روی یک دیکشنری (مثلاً دیتایی که از JSON خوندیم)
        همراه با اعتبارسنجی اولیه
        """
        # اعتبارسنجی: چک می‌کنیم که حتما id وجود داشته باشه
        if 'id' not in data:
            raise ValueError("دیتای کاربر نامعتبر است: id یافت نشد!")

        # یه کپی از دیتا می‌گیریم تا دیتای اصلی دستکاری نشه
        user_data = data.copy()

        # آیدی رو جدا می‌کنیم چون به عنوان پارامتر اصلی به کلاس میدیم
        user_id = user_data.pop('id')

        # بقیه دیتا رو به عنوان kwargs پاس می‌دیم
        return cls(id=user_id, **user_data)

    def __repr__(self):
        """
        برای اینکه وقتی کاربر رو پرینت می‌کنیم، خروجی خوانا باشه
        """
        return f"User({self.__dict__})"


# ==========================================
# بخش تست کد (بر اساس خروجی مورد انتظار توی عکست)
# ==========================================
# if __name__ == "__main__":
#     # تست با دیتاست اول (دارای name, age, city)
#     data1 = {"id": 1, "name": "Ali", "age": 25, "city": "Tehran"}
#     user1 = User.from_dict(data1)
#
#     print("--- Test 1 ---")
#     print(user1.id)  # خروجی: 1
#     print(user1.name)  # خروجی: Ali
#     print(user1.to_dict())  # خروجی به شکل دیکشنری
#
#     print("\n--- Test 2 ---")
#
#     # تست با دیتاست دوم (دارای username, gender)
#     data2 = {"id": 2, "username": "Ali123", "gender": "male"}
#     user2 = User.from_dict(data2)
#
#     print(user2.id)  # خروجی: 2
#     print(user2.username)  # خروجی: Ali123
#     print(user2.to_dict())  # خروجی به شکل دیکشنری