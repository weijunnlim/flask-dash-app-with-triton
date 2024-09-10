from dash.dependencies import Input, Output, State
from dash import html
from .inference import perform_segmentation

def segmented_image_callback(dash_app):
    @dash_app.callback(Output('segmented-image-display', 'children'),
        [Input('segmentation-btn', 'n_clicks')],
        [State('upload-image', 'contents')] #the image that we uploaded
    )
    def update_output(n_clicks, uploaded_image):
        if n_clicks is None or uploaded_image is None:
            return html.Div(), html.Div()

        return perform_segmentation(uploaded_image)