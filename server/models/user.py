class User:
    def __init__(self, id: int, name: str, email: str) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.bio = ""

    @staticmethod
    def from_clerk_user(clerk_user: dict) -> "User":
        """
        Cria uma instância de User a partir dos dados do Clerk
        """
        return User(
            id=clerk_user["id"],
            name=clerk_user.get("first_name", "")
            + " "
            + clerk_user.get("last_name", ""),
            email=clerk_user.get("email_addresses", [{}])[0].get("email_address", ""),
        )
