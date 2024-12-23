import os
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer


class LLMHandler:
    def __init__(self, model_name="gpt2", token=None):
        # Authenticate with Hugging Face if a token is provided
        if token:
            os.environ["HF_TOKEN"] = token

        # Load model and tokenizer
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
            self.model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)
            self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        except Exception as e:
            raise EnvironmentError(
                f"Failed to load model '{model_name}'. Ensure the model is valid and accessible. Error: {e}"
            )

    def generate_listing_llm(self, features, description):
        """
        Generate a real estate listing based on property features and a description.
        """
        prompt = f"Generate a real estate listing with these features: {features}. Description: {description}."
        try:
            response = self.generator(
                prompt,
                max_new_tokens=1000,  # Generate up to 150 new tokens
                num_return_sequences=1
            )
            return response[0]["generated_text"].strip()
        except Exception as e:
            return f"Error generating listing: {str(e)}"

    def generate_customer_profiles(self, features):
        """
        Generate 5 realistic customer profiles for the property features provided.
        """
        try:
            if len(features) < 7:
                raise ValueError(f"Expected at least 7 input values, but got {len(features)}.")

            # Extract relevant features for profile generation
            lot_area, overall_quality, overall_condition, central_air, full_bath, bedrooms, garage_cars = features[:7]
            price = features[-1]  # Assuming price is the last parameter

            # Generate profiles based on inputs
            profiles = []
            for i in range(1, 6):
                profile = {
                    "Customer ID": f"CUST-{i}",
                    "Occupation": self.get_occupation(overall_quality),
                    "Annual Income": f"${self.estimate_income(price):,.2f}",
                    "Family Size": self.estimate_family_size(bedrooms),
                    "Lifestyle": self.get_lifestyle(overall_condition),
                    "Interest in Property": "High" if overall_quality >= 7 else "Moderate",
                }
                profiles.append(profile)

            # Format the output as a readable string
            output = "Generated Customer Profiles:\n"
            for profile in profiles:
                output += "\n".join([f"{key}: {value}" for key, value in profile.items()]) + "\n\n"
            return output.strip()
        except Exception as e:
            return f"Error generating customer profiles: {str(e)}"

    def get_occupation(self, overall_quality):
        """
        Map overall quality to an occupation type.
        """
        if overall_quality >= 8:
            return "Executive"
        elif 6 <= overall_quality < 8:
            return "Manager"
        elif 4 <= overall_quality < 6:
            return "Engineer"
        else:
            return "Retail Worker"

    def estimate_income(self, price):
        """
        Estimate annual income based on property price.
        """
        return price * 0.3  # Assume income is approximately 30% of property price

    def estimate_family_size(self, bedrooms):
        """
        Estimate family size based on the number of bedrooms.
        """
        return min(bedrooms + 1, 6)  # Cap family size at 6 for simplicity

    def get_lifestyle(self, overall_condition):
        """
        Map overall condition to a lifestyle category.
        """
        if overall_condition >= 8:
            return "Luxury"
        elif 6 <= overall_condition < 8:
            return "Comfortable"
        elif 4 <= overall_condition < 6:
            return "Basic"
        else:
            return "Frugal"
