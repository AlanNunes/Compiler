# ===========================================================
# =     Prepare all resources necessary to compiler work    =
# ===========================================================
import os

def load_csharp_environment():
    dotNet = os.environ["WINDIR"] + "/Microsoft.NET"
    if os.path.exists(dotNet + "/Framework64"):
        if os.path.exists(dotNet + "/Framework64/v4.0.30319"):
            os.environ["CSharpComp"] = dotNet + "/Framework64/v4.0.30319"
        elif os.path.exists(dotNet + "/Framework64/v3.5"):
            os.environ["CSharpComp"] = dotNet + "/Framework64/v3.5"
    elif os.path.exists(dotNet + "/Framework"):
        if os.path.exists(dotNet + "/Framework/v4.0.30319"):
            os.environ["CSharpComp"] = dotNet + "/Framework64/v4.0.30319"
        elif os.path.exists(dotNet + "/Framework/v3.5"):
            os.environ["CSharpComp"] = dotNet + "/Framework64/v3.5"