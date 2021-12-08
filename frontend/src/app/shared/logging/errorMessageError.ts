import { ErrorElement } from '@/shared/logging'


export interface ErrorMessageError
{
    class?: string;
    status?: number;
    title?: string;
    errors?: ErrorElement[];
}