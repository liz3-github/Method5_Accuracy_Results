import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# 使用之前的calculate_accuracy函数来计算单个文件的准确率
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
    
    return {
        'Total_Rows': total_rows,
        'Onset_Time_Accuracy': onset_accuracy,
        'Timestamp_Accuracy': timestamp_accuracy,
        'Text_Accuracy': text_accuracy,
        'Language_Accuracy': lang_accuracy,
        'Speaker_Accuracy': speaker_accuracy,
        'Matching_Rows': {
            'Onset_Time': no_diff_rows,
            'Timestamp': zero_timestamp_rows,
            'Text': no_text_diff_rows,
            'Language': no_lang_diff_rows,
            'Speaker': no_speaker_diff_rows
        }
    }

def process_files():
    files = sorted(glob.glob("v*.csv"))
    all_results = []
    
    for file in files:
        filename = os.path.basename(file)
        try:
            df = pd.read_csv(file)
            results = calculate_accuracy(df)
            if results:
                results['Filename'] = filename
                all_results.append(results)
                
                # 打印每个文件的详细结果
                print(f"\nResults for {filename}:")
                print(f"Total Rows: {results['Total_Rows']}")
                print("Accuracies:")
                print(f"Onset Time Accuracy: {results['Onset_Time_Accuracy']:.2%}")
                print(f"Timestamp Accuracy: {results['Timestamp_Accuracy']:.2%}")
                print(f"Text Accuracy: {results['Text_Accuracy']:.2%}")
                print(f"Language Accuracy: {results['Language_Accuracy']:.2%}")
                print(f"Speaker Accuracy: {results['Speaker_Accuracy']:.2%}")
                print("-" * 50)
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    return all_results

def calculate_overall_statistics(all_results):
    # 创建DataFrame来存储所有结果
    df = pd.DataFrame(all_results)
    
    # 计算每列的统计量
    accuracy_cols = [col for col in df.columns if 'Accuracy' in col]
    stats = {}
    
    for col in accuracy_cols:
        metric = col.replace('_Accuracy', '')
        values = df[col]
        stats[metric] = {
            'Mean': values.mean(),
            'SD': values.std(),
            'SE': values.std() / np.sqrt(len(values)),
            'Min': values.min(),
            'Max': values.max()
        }
    
    return stats

def save_results(all_results, stats, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存每个文件的详细结果
    detailed_df = pd.DataFrame(all_results)
    detailed_df.to_csv(os.path.join(output_dir, 'detailed_results.csv'), index=False)
    
    # 保存统计结果
    stats_df = pd.DataFrame(stats).transpose()
    stats_df.to_csv(os.path.join(output_dir, 'statistics_results.csv'))
    
    # 创建可视化
    plt.figure(figsize=(12, 6))
    means = [stats[m]['Mean'] for m in stats.keys()]
    sds = [stats[m]['SD'] for m in stats.keys()]
    
    x = range(len(stats))
    plt.bar(x, means, yerr=sds, capsize=5)
    plt.xticks(x, stats.keys(), rotation=45)
    plt.title('Average Accuracy by Metric')
    plt.ylabel('Accuracy')
    
    # 添加数值标签
    for i, (mean, sd) in enumerate(zip(means, sds)):
        plt.text(i, mean, f'{mean:.2%}\n±{sd:.2%}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_summary.png'))
    plt.close()

def main():
    output_dir = "accuracy_results"
    
    # 处理所有文件
    print("Processing files...")
    all_results = process_files()
    
    # 计算整体统计量
    print("\nCalculating overall statistics...")
    stats = calculate_overall_statistics(all_results)
    
    # 打印整体统计结果
    print("\nOverall Statistics:")
    for metric, values in stats.items():
        print(f"\n{metric}:")
        print(f"Mean: {values['Mean']:.2%}")
        print(f"SD: {values['SD']:.2%}")
        print(f"SE: {values['SE']:.2%}")
        print(f"Range: {values['Min']:.2%} - {values['Max']:.2%}")
    
    # 保存结果
    save_results(all_results, stats, output_dir)
    print(f"\nResults saved to {output_dir}/")

if __name__ == "__main__":
    main()