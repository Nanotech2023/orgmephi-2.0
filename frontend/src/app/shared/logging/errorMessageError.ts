import { ErrorElement } from '@/shared/logging/index'


export interface ErrorMessageError
{
    class?: string;
    status?: number;
    title?: string;
    errors?: ErrorElement[];
}