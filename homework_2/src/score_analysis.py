"""Score Analysis Exercise""" 
import numpy as np 
import matplotlib.pyplot as plt 
 
def analyze_scores(scores):
    """
    Exercise 2: Student Score Analysis with NumPy
    ------------------------------------------
    Task: Analyze student performance across multiple subjects.
    
    Required steps:
    1. Calculate statistics for:
       - Each student's average performance
       - Each subject's average scores
       - Overall class performance
       
    2. Analyze score distribution:
       - Calculate standard deviation
       - Identify highest and lowest performing students
       - Determine score ranges for each subject
    
    3. Create visualizations:
       - Bar plot of student averages with error bars
       - Subject performance comparison
       - Score distribution histogram
       - Box plot for each subject
    
    Parameters:
    -----------
    scores : numpy.ndarray
        2D array with shape (num_students, num_subjects)
        Each row represents a student
        Each column represents a subject
    
    Expected Output:
    --------------
    1. Four-panel figure showing:
       - Student performance bar plot
       - Subject averages bar plot
       - Score distribution histogram
       - Box plot by subject
    2. Dictionary with statistical analysis
    
    Hint: Use np.mean, np.std for calculations
    """

    student_averages = np.mean(scores, axis=1)  # Student's mean
    subject_averages = np.mean(scores, axis=0)  # Subject's mean
    average = np.mean(scores)  # Overall mean

    score_std = np.std(scores)  # Standard deviation
    best_student_index = np.argmax(student_averages)  # Best student
    worst_student_index = np.argmin(student_averages)  # Worst student
    subjects_ranges = np.max(scores, axis=0)-np.min(scores, axis=0)  # Subject's ranges

    # Dictionary with statistics
    stats = {
        'Students mean': student_averages,
        'Subjects mean': subject_averages,
        'Overall mean': average,
        'Standard deviation': score_std,
        'Best student': best_student_index,
        'Worst student': worst_student_index,
        'Subjects ranges': subjects_ranges,
    }

    # Plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Students performance bar plot
    axes[0, 0].bar(np.arange(len(student_averages)), student_averages, yerr=np.std(scores, axis=1), capsize=5, color='skyblue')
    axes[0, 0].set_title('Student Average Performance')
    axes[0, 0].set_xlabel('Student Index')
    axes[0, 0].set_ylabel('Average Score')
    axes[0, 0].grid(axis='y')

    # Subject averages bar plot
    axes[0, 1].bar(np.arange(len(subject_averages)), subject_averages, color='lightgreen')
    axes[0, 1].set_title('Subject Performance Comparison')
    axes[0, 1].set_xlabel('Subject Index')
    axes[0, 1].set_ylabel('Average Score')
    axes[0, 1].grid(axis='y')

    # Score distribution histogram
    axes[1, 0].hist(scores.flatten(),color='orange', edgecolor='black', alpha=0.7)
    axes[1, 0].set_title('Score Distribution')
    axes[1, 0].set_xlabel('Score Range')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].grid(axis='y')

    # Box plot by subject
    axes[1, 1].boxplot(scores,patch_artist=True,boxprops=dict(facecolor='pink', color='black'))
    axes[1, 1].set_title('Score Range by Subject')
    axes[1, 1].set_xlabel('Subject Index')
    axes[1, 1].set_ylabel('Scores')
    axes[1, 1].grid(axis='y')

    plt.tight_layout()
    plt.show()

    return stats
