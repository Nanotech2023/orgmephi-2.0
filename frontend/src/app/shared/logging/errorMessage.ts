import { ErrorMessageError } from '@/shared/logging'


export interface ErrorMessage
{
    headers: Headers;
    status: number;
    statusText: string;
    url: string;
    ok: boolean;
    name: string;
    message: string;
    error: ErrorMessageError;
}