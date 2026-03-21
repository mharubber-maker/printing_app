# Order Status
class OrderStatus:
    PENDING   = "جارى"
    READY     = "جاهز"
    DELIVERED = "تم التسليم"

    ALL = [PENDING, READY, DELIVERED]

    COLORS = {
        PENDING:   "yellow",
        READY:     "green",
        DELIVERED: "blue",
    }


# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE     = 100

# File Upload
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
