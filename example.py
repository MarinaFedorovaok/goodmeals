from pyzbar.pyzbar import decode
from PIL import Image
import cv2
#print(cv2.__version__)

def main():
    fp = 'barcode.png'
    # image = Image.open(fp)
    # image.show()
    image = cv2.imread(fp)
    barcodes = decode(image)
    decoded = barcodes[0]
    print(decoded)
    #
    url: bytes = decoded.data
    url = url.decode()
    print(url)
    # rect
    rect = decoded.rect
    print(rect)  # Rect(left=19, top=19, width=292, height=292)

    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

        # print the barcode type and data to the terminal
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    # show the output image
    cv2.imshow("Image", image)
    # cv2.imwrite('macbook_qr_rect.jpg', image)
    cv2.waitKey(0)  # 按任意键退出 

main()