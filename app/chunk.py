import os
# 讀取小說資料
def read_data() -> str:
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "..", "data", "fiction.md")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# 將小說內容依照兩個換行符號切割，合併標題與文章內容，回傳一陣列。
def get_chunks() -> list[str]:
    content : str = read_data()
    chunks : list[str] = content.split("\n\n")

    result = []
    header = ""
    for c in chunks:
        # 如果c以雙井號開頭，將c加入header
        # 若header中有內容，且c不是以雙井號開頭，將其合併在一起
        if (c.startswith("##")):
            header = f"{c}\n"
        else:
            if (header):
                result.append(f"{header}{c}")
                header = ""
            else:
                result.append(c)

    return result

if __name__ == "__main__":
    chunks = get_chunks()
    for c in chunks:
        print(c)
        print("----------")