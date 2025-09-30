import pandas as pd
import numpy as np
import os
from django.core.files import File
import zipfile

from glccp.models import CleanedData

## For 2025
dct_field = {
    "1": "image_1",
    "r": "image_1",
    "2": "image_2",
    "3": "image_3",
    
}
## Get these backed up on AWS
fl_zip = "./glccp/glccp_photos_lte119_2025.zip"
fl_zip = "./glccp/glccp_photos_gte120_2025.zip"
# upload_photos("./glccp/glccp_photos_lte119_2025.zip")
# upload_photos("./glccp/glccp_photos_gte120_2025.zip")



def upload_photos(fl_zip):
    fl_issues = "glccp_photo_issues_2025.tsv"
    if not os.path.exists(fl_issues):
        with open(fl_issues, "wt") as f:
            f.writelines("Farm\tField\tImage\tYear\tError\tFilename\n")
    with zipfile.ZipFile(fl_zip) as myzip:
        # year = int(fl_zip.split("_")[2].replace(".zip", ""))
        year = 2025
        for i, fl in enumerate(myzip.filelist):

            print(i, fl.filename)

            farm, field = fl.filename.split("_")[0].split("-")
            photo_id = fl.filename.split(".")[0].strip()[-1]
            try:
                field_name = dct_field[photo_id]
            except KeyError:
                
                print(f"\tError!")
                print("-------------")
                
                with open(fl_issues, "at") as f:
                    f.writelines(
                        f"{farm}\t{field}\t{field_name}\t{year}\tWrong image name, likely fourth or more image\t{fl.filename}\n"
                    )
                
                break

            print(f"Farm {farm}\tfield {field}\t{field_name}\t{year}")

            try:
                glccp_record = CleanedData.objects.get(farm=farm, field=field, year=str(year))
            except CleanedData.DoesNotExist as e:
                print(f"\tError:", e)
                print("-------------")
                with open(fl_issues, "at") as f:
                    f.writelines(
                        f"{farm}\t{field}\t{field_name}\t{year}\tNo field or farm with this year\t{fl.filename}\n"
                    )
            except CleanedData.MultipleObjectsReturned as e:
                print(f"\tError:", e)
                print("-------------")
                with open(fl_issues, "at") as f:
                    f.writelines(
                        f"{farm}\t{field}\t{field_name}\t{year}\tMultiple records for this field for this year\t{fl.filename}\n"
                    )            
                
            # Commenting out for a dry run
            # with myzip.open(fl.filename) as f_img:
            #     with File(f_img, name=fl.filename) as img:
            #         setattr(glccp_record, field_name, img)
            #         glccp_record.save()
            print("-------------")


## For 2022 and 2023
dct_field = {
    "1": "image_1",
    "2": "image_2",
    "3": "image_3",
}
## Get these backed up on AWS
fl_zip = "./glccp/glccp_photos_2022.zip"
fl_zip = "./glccp/glccp_photos_2023_1.zip"
fl_zip = "./glccp/glccp_photos_2023_2.zip"

fl_issues = "glccp_photo_issues.tsv"
if not os.path.exists(fl_issues):
    with open(fl_issues, "at") as f:
        f.writelines("Farm\tField\tImage\tYear\tError\n")

with zipfile.ZipFile(fl_zip) as myzip:
    year = int(fl_zip.split("_")[2].replace(".zip", ""))
    for i, fl in enumerate(myzip.filelist):
        # if i <= 32:
        #     continue
        print(fl.filename)

        farm, field = fl.filename.split("_")[0].split("-")
        photo_id = fl.filename.split(".")[0][-1]
        try:
            field_name = dct_field[photo_id]
        except KeyError:
            print(f"\tError!")
            print("-------------")
            with open(fl_issues, "at") as f:
                f.writelines(
                    f"{farm}\t{field}\t{field_name}\t{year}\tWrong image name, likely fourth or more image\n"
                )
            continue

        print(f"Farm {farm}\tfield {field}\t{field_name}\t{year}")

        try:
            glccp_record = CleanedData.objects.get(farm=farm, field=field, year=year)
        except:
            print(f"\tError!")
            print("-------------")
            with open(fl_issues, "at") as f:
                f.writelines(
                    f"{farm}\t{field}\t{field_name}\t{year}\tNo field or farm with this year\n"
                )
            continue

        with myzip.open(fl.filename) as f_img:
            with File(f_img, name=fl.filename) as img:
                setattr(glccp_record, field_name, img)
                glccp_record.save()
        print("-------------")




dir_photos = "./glccp/photos"
dir_photos = "./photos"

photos = os.listdir(dir_photos)

dct_field = {
    "1": "image_1",
    "2": "image_2",
    "3": "image_3",
}

for fl_photo in photos:

    farm, field = fl_photo.split("_")[0].split("-")
    photo_id = fl_photo.split(".")[0][-1]
    field_name = dct_field[photo_id]
    glccp_record = CleanedData.objects.get(farm=farm, field=field, year=year)

    with File(open(os.path.join(dir_photos, fl_photo), "rb"), name=fl_photo) as img:
        setattr(glccp_record, field_name, img)
        glccp_record.save()


fl_zip = "/home/evans/Downloads/glccp_photos_2022.zip"


with zipfile.ZipFile(fl_zip) as myzip:
    for i, fl in enumerate(myzip.filelist):
        print(fl.filename)
        if i == 19:
            break
        with myzip.open(fl.filename) as f_img:
            with File(f_img, name=fl.filename) as img:
                setattr(glccp_record, field_name, img)
                glccp_record.save()
