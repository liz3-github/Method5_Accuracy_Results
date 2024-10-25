import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

def calculate_accuracy(df):
    
    total_rows = len(df)
    
    if total_rows == 0:
        return None
        
    # 1. Onset Time Accuracy - 直接用'No difference'计算
    no_diff_rows = df['Absolute_onset_time_difference'].eq('No difference').sum()
    onset_accuracy = no_diff_rows / total_rows
    
    # 2. Timestamp Accuracy - 直接用'00:00:00'计算
    zero_timestamp_rows = df['TimeStamp_difference'].eq('00:00:00').sum()
    timestamp_accuracy = zero_timestamp_rows / total_rows
    
    # 3. Text Accuracy
    no_text_diff_rows = df['text_difference'].eq(False).sum()
    text_accuracy = no_text_diff_rows / total_rows
    
    # 4. Language Accuracy
    no_lang_diff_rows = df['language_difference'].eq(False).sum()
    lang_accuracy = no_lang_diff_rows / total_rows
    
    # 5. Speaker Accuracy
    no_speaker_diff_rows = df['Speaker_difference'].eq(False).sum()
    speaker_accuracy = no_speaker_diff_rows / total_rows
    
    results = {
        'Total_Rows': total_rows,
        'Onset_Time': {
            'matching_rows': no_diff_rows,
            'total_rows': total_rows,
            'accuracy': onset_accuracy
        },
        'Timestamp': {
            'matching_rows': zero_timestamp_rows,
            'total_rows': total_rows,
            'accuracy': timestamp_accuracy
        },
        'Text': {
            'matching_rows': no_text_diff_rows,
            'total_rows': total_rows,
            'accuracy': text_accuracy
        },
        'Language': {
            'matching_rows': no_lang_diff_rows,
            'total_rows': total_rows,
            'accuracy': lang_accuracy
        },
        'Speaker': {
            'matching_rows': no_speaker_diff_rows,
            'total_rows': total_rows,
            'accuracy': speaker_accuracy
        }
    }
    
    # 打印详细分析
    print("\nDetailed Analysis:")
    print(f"Total valid rows: {total_rows}")
    print(f"'No difference' rows: {no_diff_rows} ({onset_accuracy:.2%})")
    print(f"'00:00:00' timestamp rows: {zero_timestamp_rows} ({timestamp_accuracy:.2%})")
    print(f"No text difference rows: {no_text_diff_rows} ({text_accuracy:.2%})")
    print(f"Same language rows: {no_lang_diff_rows} ({lang_accuracy:.2%})")
    print(f"Same speaker rows: {no_speaker_diff_rows} ({speaker_accuracy:.2%})")
    
    return results

def main():
    try:
        filenames = ['v002.csv']  # 你可以添加更多文件名
        
        for filename in filenames:
            print(f"\nProcessing {filename}:")
            df = pd.read_csv(filename)
            results = calculate_accuracy(df)
            
            if results:
                print(f"\nTotal Rows (excluding markers): {results['Total_Rows']}")
                
                print("\nAccuracy Results:")
                metrics = ['Onset_Time', 'Timestamp', 'Text', 'Language', 'Speaker']
                for metric in metrics:
                    print(f"\n{metric}:")
                    print(f"Matching Rows: {results[metric]['matching_rows']}")
                    print(f"Total Rows: {results[metric]['total_rows']}")
                    print(f"Accuracy: {results[metric]['accuracy']:.2%}")
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()