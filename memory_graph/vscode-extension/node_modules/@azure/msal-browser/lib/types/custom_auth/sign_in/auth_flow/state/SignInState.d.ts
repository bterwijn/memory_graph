import { AuthFlowActionRequiredStateBase } from "../../../core/auth_flow/AuthFlowState.js";
import { SignInStateParameters } from "./SignInStateParameters.js";
export declare abstract class SignInState<TParameters extends SignInStateParameters> extends AuthFlowActionRequiredStateBase<TParameters> {
    constructor(stateParameters: TParameters);
}
//# sourceMappingURL=SignInState.d.ts.map