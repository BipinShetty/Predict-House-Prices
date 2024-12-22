import gradio as gr

class RealEstateAppUI:
    def __init__(self, app):
        self.app = app

    def create_ui(self):
        with gr.Blocks() as demo:
            gr.Markdown("# Real Estate Application")

            with gr.Tab("Sale Price Estimation and Recording"):
                with gr.Row():
                    estimation_inputs = [
                        gr.Number(label="Lot Area"),
                        gr.Number(label="Overall Quality"),
                        gr.Number(label="Overall Condition"),
                        gr.Radio(["Y", "N"], label="Central Air"),
                        gr.Number(label="Full Bath"),
                        gr.Number(label="Bedrooms"),
                        gr.Number(label="Garage Cars"),
                    ]
                    predicted_price = gr.Textbox(label="Predicted Price")
                    gr.Button("Predict").click(
                        self.app.predict_price, inputs=estimation_inputs, outputs=predicted_price
                    )

                with gr.Row():
                    record_inputs = [
                        gr.Number(label="Price"),
                        *estimation_inputs
                    ]
                    recorded_price = gr.Textbox(label="Recorded Price")
                    gr.Button("Record Sale").click(
                        self.app.record_price, inputs=record_inputs, outputs=recorded_price
                    )

            with gr.Tab("Sales Listing and Customer Profiling"):
                query_inputs = [
                    gr.Number(label="Lot Area"),
                    gr.Number(label="Overall Quality"),
                    gr.Number(label="Overall Condition"),
                    gr.Radio(["Y", "N"], label="Central Air"),
                    gr.Number(label="Full Bath"),
                    gr.Number(label="Bedrooms"),
                    gr.Number(label="Garage Cars"),
                ]
                closest_match_output = gr.Textbox(label="Closest Match Property")
                gr.Button("Query Closest Match").click(
                    self.app.query_closest_match, inputs=query_inputs, outputs=closest_match_output
                )

                with gr.Row():
                    description = gr.Textbox(label="Property Description")
                    listing_output = gr.Textbox(label="Generated Listing")
                    gr.Button("Generate Listing").click(
                        self.app.generate_listing,
                        inputs=[*query_inputs, description],
                        outputs=listing_output,
                    )

                with gr.Row():
                    feedback = gr.Radio(["Thumbs Up", "Thumbs Down"], label="Feedback")
                    feedback_output = gr.Textbox(label="Feedback Recorded")
                    gr.Button("Submit Feedback").click(
                        self.app.record_feedback,
                        inputs=[listing_output, feedback],
                        outputs=feedback_output,
                    )

                with gr.Row():
                    customer_profiles_output = gr.Textbox(label="Customer Profiles", lines=10)
                    gr.Button("Generate Customer Profiles").click(
                        self.app.generate_customer_profiles,
                        inputs=query_inputs,
                        outputs=customer_profiles_output,
                    )

        demo.launch()
