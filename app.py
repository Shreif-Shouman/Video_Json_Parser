import streamlit as st
import json

def extract_transcripts(json_data):
    transcripts = []
    annotation_results = json_data.get("annotation_results", [])

    for annotation in annotation_results:
        speech_transcriptions = annotation.get("speech_transcriptions", [])
        for transcription in speech_transcriptions:
            alternatives = transcription.get("alternatives", [])
            for alternative in alternatives:
                transcript = alternative.get("transcript", "")
                if transcript:
                    transcripts.append(transcript)

    return transcripts

def main():
    st.title("Video Intelligence API JSON Parser")

    # Upload JSON file
    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

    if uploaded_file is not None:
        try:
            # Load JSON data
            json_data = json.load(uploaded_file)

            # Extract and display transcripts without "Transcript X:"
            transcripts = extract_transcripts(json_data)

            if transcripts:
                st.subheader("Transcripts")
                for i, transcript in enumerate(transcripts):
                    # Split the transcript by line breaks and display each line
                    lines = transcript.strip().split('\n')
                    for line in lines:
                        st.write(line.strip())

                # Add a download button to save the transcripts as a .txt file
                st.markdown(
                    f"### Download Transcripts as .txt File\n"
                    f"Click the button below to download the transcripts as a .txt file."
                )
                txt_transcripts = "\n".join(transcripts)
                st.download_button(
                    label="Download Transcripts",
                    data=txt_transcripts,
                    key="download-txt",
                    file_name="transcripts.txt",
                    mime="text/plain",
                )

            else:
                st.warning("No transcripts found in the JSON file.")

        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid JSON file.")
    else:
        st.info("Please upload a JSON file.")

if __name__ == "__main__":
    main()
