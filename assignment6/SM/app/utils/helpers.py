import os
import secrets
from flask import render_template, current_app, redirect, url_for


def render_error_page(error_message, errorcode=500):
    if errorcode == 500:
        return (
            render_template("500.html", error_message=error_message),
            errorcode,
        )
    return (
        render_template("error.html", error_message=error_message),
        errorcode,
    )


def load_next_page(request):
    next_page = request.args.get("next") or request.form.get("next")
    if next_page:
        return redirect(next_page)
    else:
        return redirect(url_for("general.home"))


def save_image(image):
    image_upload_folder = current_app.config["IMAGE_UPLOAD_FOLDER"]
    default_image_url = current_app.config["DEFAULT_IMAGE_URL"]
    root_dir = current_app.config["ROOT_DIR"]

    image_folder_path = os.path.join(os.getcwd(), root_dir, image_upload_folder)
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)

    if image:
        image_filename = f"{secrets.token_hex(8)}_{image.filename}"
        image_path = os.path.join(image_folder_path, image_filename)
        image.save(image_path)
        image_url = f"/{image_upload_folder}/{image_filename}"
    else:
        image_url = default_image_url  # Set to default image if no image is uploaded

    return image_url
