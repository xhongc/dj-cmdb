class ValueTypeEnum:
    INT = "0"
    FLOAT = "1"
    TEXT = "2"
    DATETIME = "3"
    DATE = "4"
    TIME = "5"
    JSON = "6"
    CHAR = "7"


VALUE_TYPE_MAP = (
    (ValueTypeEnum.INT, "整型"),
    (ValueTypeEnum.FLOAT, "浮点型"),
    (ValueTypeEnum.TEXT, "文本型"),
    (ValueTypeEnum.DATETIME, "日期时间"),
    (ValueTypeEnum.DATE, "日期"),
    (ValueTypeEnum.TIME, "时间"),
    (ValueTypeEnum.JSON, "JSON"),
    (ValueTypeEnum.CHAR, "字符串"),
)
