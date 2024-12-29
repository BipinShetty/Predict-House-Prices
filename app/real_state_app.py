import gradio as gr


class RealEstateAppUI:
    def __init__(self, app):
        self.app = app

    def create_ui(self):
        with gr.Blocks() as demo:
            gr.Markdown("# 🏡 Real Estate Application")
            gr.Markdown("A modern interface for property price estimation, customer profiling, and more.")

            # Tab: Sale Price Estimation and Recording
            with gr.Tab("💰 Sale Price Estimation and Recording"):
                with gr.Row():
                    gr.Markdown("### Predict and Record Sale Price")

                with gr.Row():
                    estimation_inputs = [
                        gr.Number(label="Lot Area (sq ft)"),
                        gr.Number(label="Overall Quality (1-10)"),
                        gr.Number(label="Overall Condition (1-10)"),
                        gr.Radio(["Y", "N"], label="Central Air"),
                        gr.Number(label="Full Bathrooms"),
                        gr.Number(label="Bedrooms"),
                        gr.Number(label="Garage Cars"),
                    ]
                    predicted_price = gr.Textbox(label="Predicted Price", placeholder="Estimated sale price will appear here")
                    gr.Button("🔮 Predict").click(
                        self.app.predict_price, inputs=estimation_inputs, outputs=predicted_price
                    )

                with gr.Row():
                    record_inputs = [
                        gr.Number(label="Sale Price ($)", placeholder="Enter the verified sale price"),
                        *estimation_inputs
                    ]
                    recorded_price = gr.Textbox(label="Recorded Price", placeholder="Sale price record confirmation")
                    gr.Button("💾 Record Sale").click(
                        self.app.record_price, inputs=record_inputs, outputs=recorded_price
                    )

            # Tab: Sales Listing and Customer Profiling
            with gr.Tab("📄 Sales Listing and Customer Profiling"):
                gr.Markdown("### Explore Property Listings and Customer Insights")

                with gr.Row():
                    query_inputs = [
                        gr.Number(label="Lot Area (sq ft)"),
                        gr.Number(label="Overall Quality (1-10)"),
                        gr.Number(label="Overall Condition (1-10)"),
                        gr.Radio(["Y", "N"], label="Central Air"),
                        gr.Number(label="Full Bathrooms"),
                        gr.Number(label="Bedrooms"),
                        gr.Number(label="Garage Cars"),
                    ]
                    closest_match_output = gr.Textbox(label="Closest Match Property", placeholder="Matching property details will appear here")
                    gr.Button("🔍 Query Closest Match").click(
                        self.app.query_closest_match, inputs=query_inputs, outputs=closest_match_output
                    )

                gr.Markdown("#### 🏠 Generate Property Listing")
                with gr.Row():
                    description = gr.Textbox(label="Property Description", placeholder="Describe the property in detail")
                    listing_output = gr.Textbox(label="Generated Listing", placeholder="AI-generated property listing will appear here")
                    gr.Button("📝 Generate Listing").click(
                        self.app.generate_listing,
                        inputs=[*query_inputs, description],
                        outputs=listing_output,
                    )

                gr.Markdown("#### 📋 Submit Feedback for Listings")
                with gr.Row():
                    feedback = gr.Radio(["👍 Thumbs Up", "👎 Thumbs Down"], label="Feedback", type="value")
                    feedback_output = gr.Textbox(label="Feedback Status", placeholder="Feedback submission status will appear here")
                    gr.Button("✅ Submit Feedback").click(
                        self.app.record_feedback,
                        inputs=[listing_output, feedback],
                        outputs=feedback_output,
                    )

                gr.Markdown("#### 👥 Generate Customer Profiles")
                with gr.Row():
                    customer_profiles_output = gr.Textbox(label="Customer Profiles", lines=10, placeholder="Customer profiles will be displayed here")
                    gr.Button("👥 Generate Profiles").click(
                        self.app.generate_customer_profiles,
                        inputs=query_inputs,
                        outputs=customer_profiles_output,
                    )

        demo.launch()
