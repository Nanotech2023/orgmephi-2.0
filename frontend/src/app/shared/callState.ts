export const enum LoadingState
{
    INIT = "INIT",
    LOADING = "LOADING",
    LOADED = "LOADED"
}


export interface ErrorState
{
    errorMessage: string;
}


export type CallState = LoadingState | ErrorState;


export function getError( callState: CallState ): LoadingState | string | null
{
    return ( callState as ErrorState ).errorMessage === undefined ? null : ( callState as ErrorState ).errorMessage
}