import streamlit as st
import pandas as pd
import fasttext
import io
from PIL import Image

# Loading Image using PIL
im = Image.open('icon.png')

# Adding Image to web app
st.set_page_config(page_title="SpamScanner", page_icon = im, layout="wide")

# Load the model from the file
model = fasttext.load_model('supervised_model.bin')

# Define the predict_spam function
def predict_spam(message):
    # Predict the label of the message
    prediction = model.predict(message)
    label = prediction[0][0]  # Get the predicted label
    accuracy = prediction[1][0]
    return label, accuracy

# Streamlit application

def main():
    
    # Apply custom CSS for vertical centering
    st.markdown(
        """
        <style>
        .centered-content {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 15vh; /* Adjust the height as needed */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create a home page with centered image, text, and button
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    if st.session_state.page == 'home':
        st.markdown('<div class="centered-content">', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 3])  # Adjust the column width ratio as needed

        with col1:
            
            # Apply custom CSS for styling
            st.markdown(
                """
                <style>
                .welcome-text {
                    font-family: sans-serif;
                    text-align: left; /* Align text to the left */
                    padding: 20px;
                }
                .welcome-text h2 {
                    font-family: sans-serif;
                    font-size: 2rem;
                    margin-bottom: 10px;
                }
                .welcome-text p, ul {
                    font-family: sans-serif;
                    font-size: 1.1rem;
                    line-height: 1.7;
                    margin-bottom: 20px;
                }
                .highlight {
                    font-family: sans-serif;
                    color: #eea94d;
                    font-weight: bold;
                }
                .singlemessage {
                    font-family: sans-serif;
                    color: #56c76e;
                    font-weight: bold;
                }
                .bulkmessage {
                    font-family: sans-serif;
                    color: #e16189;
                    font-weight: bold;
                }
                .note {
                    font-family: sans-serif;
                    color: #be554b;
                    font-weight: bold;
                }
                
                </style>
                """,
                unsafe_allow_html=True
            )

            # Embed the HTML content
            st.markdown(
                """
                <div class="welcome-text">
                    <h2>Welcome to <span class="highlight">SpamScanner</span>!</h2>
                    <p>Are you curious whether a message is spam or not? Our app has you covered!</p>
                    <p><strong>Here’s what you can do:</strong></p>
                    <ul>
                        <li><span class="singlemessage">Single Message Check:</span> <p> Enter any message in the textbox to instantly find out if it’s spam or not. It’s quick and easy! </p> </li>
                        <li><span class="bulkmessage">Bulk Upload:</span> <p> Have multiple messages to check? Upload a CSV file containing a list of messages, and we’ll process them all at once. You’ll get a detailed table with each message and its spam status. </p> </li>
                    </ul>
                    <p>Effortlessly manage your messages and keep your inbox clean with <span class="highlight">SpamScanner</span>!</p>
                    <p><span class="note"><strong>Note: </strong></span>For enhanced interactivity, please double-click each button.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
            # Handle button click
            if st.button("**Enter the Application**", type="primary"):
                st.session_state.page = 'app'


        with col2:
            st.image("home.png", use_column_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == 'app': 
        if st.button("**Back to home**", type="primary"):
                st.session_state.page = 'home'
                
        st.write("<h1 style='font-size: 42px; color: #eea94d; font-family: sans-serif;'>SpamScanner</h1>", unsafe_allow_html=True)

        # Radio button for selecting mode
        mode = st.radio("**Select Check Mode:**", ["Single Message", "Bulk Messages"], horizontal=True)

        if mode == "Single Message":
        
            # Display text area with a bold label
            message = st.text_area(
                label="**Enter your message:**",  # Bold label using Markdown
                height=1,  # Optional: adjust height as needed
                placeholder="Type your message here...",  # Optional: placeholder text
                help="Type your message to check if it is spam or not.",  # Optional: tooltip text
                label_visibility="visible"  # Optional: visibility of the label
            )

            message = message.replace('\n', ' ').strip()
            
            
            if st.button("**Check**", type="primary"):
                if message:
                    # Predict and display result
                    label, accuracy = predict_spam(message)
                    accuracy_rounded = round(accuracy, 4)  # Round accuracy to 2 decimal places
                    
                    st.write(f"<p style='font-size: 16px; font-family: sans-serif;'> <strong>Accuracy Score:</strong> <strong>{accuracy_rounded}</strong></p>", unsafe_allow_html=True)
                    
                    if label == '__label__spam':
                        st.write(
                            "<p style='font-size: 18px; font-family: sans-serif;'><strong>This message is classified as SPAM.</strong></p>"
                            "<p style='font-size: 16px; font-family: sans-serif;'>"
                            "<strong> Note: </strong>The Accuracy score indicates the confidence level in the classification result. "
                            "An Accuracy score close to 1 signifies a high degree of certainty in the classification's correctness. "
                            "</p>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.write(
                            "<p style='font-size: 18px; font-family: sans-serif;'><strong>This message is classified as NOT SPAM.</strong></p>"
                            "<p style='font-size: 16px; font-family: sans-serif;'>"
                            "<strong> Note: </strong>The Accuracy score indicates the confidence level in the classification result. "
                            "An Accuracy score close to 1 signifies a high degree of certainty in the classification's correctness. "
                            "</p>",
                            unsafe_allow_html=True
                        )
                else:
                    st.write("<p style='font-size: 16px; font-family: sans-serif;'> <strong>Please enter a message.</strong></p>", unsafe_allow_html=True)


        elif mode == "Bulk Messages":
            # Upload CSV file
            uploaded_file = st.file_uploader(
                label="**Upload a CSV file with a single column of messages**",  # Bold label using Markdown
                type="csv",  # Restrict to CSV files
                help="This file should contain a single column with messages to be classified.",  # Tooltip text
                label_visibility="visible"  # Ensure the label is visible
            )

            if uploaded_file is not None:
                
                st.write( "You uploaded", uploaded_file.name, " successfully")
                
                # Read the CSV file
                df = pd.read_csv(uploaded_file)
                
                # Ensure the CSV has only one column
                if df.shape[1] != 1:
                    st.error("The CSV file should have exactly one column.")
                    return
                
                if st.button("**Classify Now**", type="primary"):
                    st.session_state.page = 'table'
                    st.session_state.df = df

    
    if st.session_state.page == 'table':
        
        df = st.session_state.df
        
        # Replace values in the 'Label' column
        

        # Process each message and classify it
        df['Label'] = df.iloc[:, 0].apply(lambda x: predict_spam(x)[0])
        
        df['Label'] = df['Label'].replace({'__label__ham': 'HAM', '__label__spam': 'SPAM'})

        # Rename columns for clarity
        df.columns = ['Message', 'Label']
                
        # Display the result in a table
        st.write("**Classification Results:**")
        st.table(df)
        
        # Convert DataFrame to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        # Provide download button
        st.download_button(
            label="**Download CSV**",
            data=csv_buffer.getvalue(),
            file_name="SpamScannerPredictions.csv",
            mime="text/csv", 
            type="primary"
        )
                
         # Handle button click
        if st.button("**Back to app**", type="primary"):
            st.session_state.page = 'app'    
              
if __name__ == "__main__":
    main()


