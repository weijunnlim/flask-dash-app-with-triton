from dash.dependencies import Input, Output, State
from dash import html
import uuid
import os
import base64

UPLOAD_FOLDER = '/home/dxd_wj/model_serving/flask-dash-app/main_app/uploads'

def register_image_upload_callback(dash_app):
    @dash_app.callback(Output('output-image-upload', 'children'),
        [Input('upload-image', 'contents')],
        [State('upload-image', 'filename')]
    )
    def update_output(image_contents, image_filename):
      if image_contents is not None and allowed_file(image_filename):
        # Decode the base64 encoded image contents
        try:
            header, base64_data = image_contents.split(',')
            image_data = base64.b64decode(base64_data)
        except Exception as e:
            return html.Div([
                html.H4("Error decoding the image."),
                html.P(str(e))
            ])
        # Save the uploaded image
        image_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{image_filename}")
        try:
            with open(image_path, "wb") as f:
                f.write(image_data)
        except Exception as e:
            return html.Div([
                html.H4("Error saving the image."),
                html.P(str(e))
            ])

        return html.Div([
            html.H5(f"Uploaded Image: {image_filename}"),
            html.Img(src=image_contents, style={
                'maxWidth': '100%',
                'height': '80vh',
                'border': '1px solid #ccc',
                'borderRadius': '10px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
            }),
            html.Hr(),
        ])
    def allowed_file(filename):
      ALLOWED_EXTENSIONS = {'png', 'jpeg', 'gif', 'jpg'}
      return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS