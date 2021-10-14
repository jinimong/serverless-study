import os
import json
import boto3
import qrcode
from PIL import Image, ImageDraw, ImageFont


def lambda_handler(event, context):
    # S3에서 필요한 파일 불러오기
    s3 = boto3.resource("s3")
    s3.Object(os.environ["BUCKET_NAME"], "imgs/cat.jpg").download_file(
        "/tmp/logo.jpg"
    )
    s3.Object(
        os.environ["BUCKET_NAME"], "fonts/summer-calling.ttf"
    ).download_file("/tmp/font.ttf")

    records = event["Records"]
    if records:
        user_id = records[0]["Sns"]["Message"]
        conf_type = records[0]["Sns"]["Subject"]

    # dynamodb 에서 데이터 불러오기
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])
    row = table.get_item(Key={"user_id": user_id, "type": conf_type})
    item = row["Item"]
    save_path = "/tmp/image.jpg"
    key = f"qrcodes/{user_id}/{conf_type}/qrcode.jpg"

    # 이미지 생성 후 S3 업로드
    make_image(data=item, save_path=save_path)
    s3.meta.client.upload_file(
        save_path,
        os.environ["BUCKET_NAME"],
        key,
        ExtraArgs={"ContentType": "image/jpeg"},
    )

    return {"statusCode": 200, "event": event}


def make_image(data, save_path):
    W, H = (400, 400)

    # logo img
    logo = Image.open("/tmp/logo.jpg").convert("RGBA")
    ttf = "/tmp/font.ttf"

    # qrcode img
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )

    qr.add_data(data.get("phone_number", ""))
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # merge
    img = Image.new("RGB", (W, H), color="#fff")
    img.paste(logo, (0, 0), logo)
    img.paste(qr_img, (270, 50))

    # draw
    font_m = ImageFont.truetype(ttf, 15)
    font_b = ImageFont.truetype(ttf, 18)
    font_B = ImageFont.truetype(ttf, 19)

    draw = ImageDraw.Draw(img)

    draw.text((50, 240), data.get("user_name", ""), fill="#000", font=font_b)
    company_name = data.get("company_name", "")
    draw.text((50, 280), f"From {company_name}", fill="#000", font=font_m)
    draw.text((20, 200), "FULL CONFERENCE PASS", fill="#ed244b", font=font_B)

    img.save(save_path, quality=100)
