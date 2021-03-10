import pandas as pd
from sklearn.metrics import plot_confusion_matrix, accuracy_score, recall_score, precision_score, f1_score, roc_curve

savedir = "models/results"

def get_results(my_name, my_model, X_test, y_test):
    print("### " + "Model for " + my_name + " ###" + "\n")

    y_pred_proba = my_model.predict_proba(X_test)[:,1] #return probabilities

    score_accuracy = accuracy_score(y_test, y_pred)
    score_recall = recall_score(y_test, y_pred)
    score_precision = precision_score(y_test, y_pred)
    score_f1 = f1_score(y_test,y_pred)
    print (f"Accuracy:       {score_accuracy}")
    print (f"Recall:         {score_recall}")
    print (f"Precision:      {score_precision}")
    print (f"F1:             {score_f1}")

    scores = pd.DataFrame(columns=['Accuracy', 'Recall', 'Precision', 'F1'],
                          data = [[score_accuracy, score_recall, score_precision, score_f1]])
    scores.to_csv(savedir + 'scores_' + my_name + '.csv')
    scores.to_latex(savedir + 'scores_' + my_name + '.tex', float_format='%.2g')

    plot_confusion_matrix(my_model, X_test, y_test)
    plt.show()

    return scores
