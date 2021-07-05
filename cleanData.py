import numpy as np
import pandas as pd

from getCPI import getCPI
from getIntRate import getIntRate


def cleanData():
    df1 = pd.read_csv("data/sample/sampleAccepted.csv")
    df1 = df1.drop(columns=["member_id", "url"])

    features = df1.loc[:, [
        "term", # Número de pagamentos pagamentos no plano
        "annual_inc", # Renda Anual
        "annual_inc_joint", # Renda anual conjunta se o empréstimo é conjunto
        "emp_length", # Tempo no emprego
        "issue_d", # data do empréstimo, para comparar com a taxa de juros básica
        "purpose", # objetivo
        "dti", # Debt-to-income <https://www.investopedia.com/terms/d/dti.asp>
        "delinq_2yrs", # 'faltas' no pagamento nos últimos 2 anos
        "open_acc", # Número de linhas de crédito abertas no histórico do cliente
        "open_il_12m", # Número de contas de prestação abertas nos últimos 12m
        "open_rv_12m", # Número de contas de crédtio rotativo abertas nos últimos 12m
        "pub_rec", # Number of derogatory public records
        "revol_util", # Fração do crédito giratório disponível sendo usado
        "chargeoff_within_12_mths", # número de declarações de 'improvável pagar' nos últimos 12m
        "mort_acc", # número de hipotecas
        "num_accts_ever_120_pd", # número de contas que já foram atrasadas a mais de 120 dias
        "num_tl_120dpd_2m", # número de contas atualmente atrasadas mais de 120 dias(atualizadas nos últimos 2 meses)
        "num_tl_30dpd", # Número de contas atualemente atrasadas mais de 30 dias
        "percent_bc_gt_75", # fração de contas acima de 75% do limite
        ]]


    def formatTerm(line):
        line = line.strip()
        line = line.split(" ")

        if line[-1] == "months":
            line = int(line[0])/12

        else:
            raise NotImplementedError(f"{line[-1]} não implementado ainda")

        return line

    features["term"] = features["term"].apply(formatTerm)

    features = features.join(pd.get_dummies(df1["home_ownership"]))
    features = features.drop(columns="OWN")

    ownership = ["ANY", "MORTGAGE", "NONE", "OTHER", "RENT"]

    def formatEmpLength(line):
        """ Testa se o indivíduo está a mais de dois anos no trabalho atual """
        Accept = ["3 years", "2 years", "8 years", "10+ years", "4 years", "6 years", "5 years", "9 years", "7 years"]
        NotAccept = ["1 year", "< 1 year", np.nan]

        if line in Accept:
            return 1
        elif line in NotAccept:
            return 0
        else:
            raise NotImplementedError(f"{line} não implementado ainda na função cleanEmpLength")

    features["emp_length"] = features["emp_length"].apply(formatEmpLength)
    features = features.rename(columns={"emp_length": "long_job"})

    def toIntPurpose(line):
        goodList = ["small_business", "renewable_energy", "home_improvement", "major_purchase", "moving", "house", "car"]
        badList = ["debt_consolidation", "credit_card", "medical"]
        neutralList = ["other", "vacation", "wedding"]

        if line in goodList:
            return 1

        elif line in badList:
            return -1

        elif line in neutralList:
            return 0

        else:
            raise NotImplementedError(f"Purpose {line} não está em nenhuma categoria")

    features = features.join(
        pd.get_dummies(
        features["purpose"]
        .apply(toIntPurpose))
        .rename(columns={
            -1: "BadPurpose",
            0: "NeutralPurpose",
            1: "GoodPurpose"
            })
        )

    features = features.drop(columns="purpose")

    def formatJointIncome(line):
        if np.nan_to_num(line) == 0:
            return 0
        
        else:
            return float(line)

    features["annual_inc_joint"] = features["annual_inc_joint"].apply(formatJointIncome).apply(np.nan_to_num)



    cpi = getCPI()
    intRate = getIntRate()

    extInf = pd.merge(left=cpi, right=intRate, left_on="date", right_on="date")
    features["issue_d"] = pd.to_datetime(features["issue_d"])
    features = pd.merge(left=features, right=extInf, left_on="issue_d", right_on="date")
    features = features.drop(columns=["date", "issue_d"])


    def formatDelinq(line):
        if line == 0:
            return 0

        elif line >= 0:
            return 1
        
        else:
            raise NotImplementedError(f"Valor inválido: {line}")

    features["delinq_2yrs"] = features["delinq_2yrs"].apply(formatDelinq)
    features = features.rename(columns={"delinq_2yrs": "delinq"})


    def formatOpenAcc(line):
        if line in [1, 2]:
            return 1

        elif line > 2:
            return 0
        
        else:
            raise NotImplementedError(f"Valor inválido para OpenAcc: {line}")

    features["recent"] = features["open_acc"].apply(formatOpenAcc)
    features = features.drop(columns="open_acc")

    def formatSecondOpenAcc(line):
        if line >= 2:
            return 1
        
        elif line >= 0 and line < 2:
            return 0
        
        elif np.nan_to_num(line, nan=-1) == -1:
            return np.NaN

        else:
            raise NotImplementedError(f"Número de contas abertas inválidas, valor que causou o erro: {line}")

    openAcc = features["open_il_12m"] + features["open_rv_12m"] + features["mort_acc"]
    features["multiplasContas"] = openAcc.apply(formatSecondOpenAcc)
    features = features.drop(columns=["open_il_12m", "open_rv_12m", "mort_acc"])

    def formatPubRec(line):
        if line >= 1:
            return 1
        
        elif line == 0:
            return 0
        
        else:
            raise NotImplementedError(f"Entrada inválida em PubRec, valor que causou o erro: {line}")

    features["bad_rec"] = features["pub_rec"].apply(formatPubRec)
    features = features.drop(columns="pub_rec")

    def formatRevolUtil(line):
        if line >= 30:
            return 1

        elif line < 30:
            return 0

        elif np.nan_to_num(line, nan=-1) == -1:
            return np.NaN

        else:
            raise NotImplementedError(f"Entrada inválida em revol_util, valor que causou o erro: {line}")

    features["badRevolUtil"] = features["revol_util"].apply(formatRevolUtil)

    def almostBadCard(line):
        if line > 0:
            return 1
        
        elif line == 0:
            return 0
        
        elif np.nan_to_num(line, nan=-1) == -1:
            return np.NaN

        else:
            raise ValueError(f"valor inválido na coluna percent_bc_gt_75, valor que causou o erro: {line}")

    features["percent_bc_gt_75"] = features["percent_bc_gt_75"].apply(almostBadCard)

    almostBroke = features["percent_bc_gt_75"] + features["badRevolUtil"]

    def formatAlmostBroke(line):
        if line >= 1:
            return 1

        elif line == 0:
            return 0

        elif np.nan_to_num(line, nan=-1) == -1:
            return np.NaN

        else:
            raise NotImplementedError(f"Entrada inválida em almostBroke, valor que causou o erro: {line}")

    features = features.drop(columns=["revol_util", "percent_bc_gt_75", "badRevolUtil"])

    features["almostBroken"] = almostBroke.apply(formatAlmostBroke)

    def formatChargeOff(line):
        if line > 0:
            return 1
        
        elif line == 0:
            return 0
        
        else:
            raise NotImplementedError(f"Entrada inválida em chargeoff_within_12_mths, valor que causou o erro: {line}")

    features["chargeOff"] = features["chargeoff_within_12_mths"].apply(formatChargeOff)
    features = features.drop(columns="chargeoff_within_12_mths")


    overDue = features["num_accts_ever_120_pd"] + features["num_tl_120dpd_2m"] + features["num_tl_30dpd"]
    features = features.drop(columns=["num_accts_ever_120_pd", "num_tl_120dpd_2m", "num_tl_30dpd"])

    def formatOverDue(line):
        if line > 0:
            return 1
        
        elif line == 0:
            return 0
        
        elif np.nan_to_num(line, nan=-1) == -1:
            return np.NaN

        else:
            raise ValueError(f"Entrada inválida em uma das seguintes colunas = [num_accts_ever_120_pd, num_tl_120dpd_2m, num_tl_30dpd],             Valor que causou o erro: {line}")

    features["overDue"] = overDue.apply(formatOverDue)

    target = df1.loc[:, ["int_rate", "grade", "loan_status"]]

    maskGradeToNum = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
        "E": 5,
        "G": 6,
    }

    target["grade"] = target["grade"].map(maskGradeToNum)

    maskLoanStatus = {
        "Late (31-120 days)": 1,
        "Late (16-30 days)": 1,
        "Charged Off": -1,
        "Does not meet the credit policy. Status:Charged Off": -1,
        "Fully Paid": 0,
        "Does not meet the credit policy. Status:Fully Paid": 0,
        "Current": 2,
        "In Grace Period": 2
    }

    target["loan_status"] = target["loan_status"].map(maskLoanStatus)


    tarDummy = pd.get_dummies(target["loan_status"])
    tarDummy = tarDummy.rename(
        columns={
            -1: "chargedOff",
            0: "paid",
            1: "late",
            2: "current"
        })

    target = target.join(tarDummy)
    target = target.drop(columns="loan_status")

    target["prob"] = target["chargedOff"] + target["late"]

    df = target.join(features)

    df = df.drop(columns=["multiplasContas", "cpi", "NeutralPurpose"])
    
    return df
