import notify from 'devextreme/ui/notify'
import { ErrorMessage } from '@/shared/logging/index'


const displayMessageTime = 4000


export function displayErrorMessage( message: ErrorMessage ): void
{
    if ( message.error.errors )
    {
        const formattedMessage: string = message.error.errors.map( item => `${ item.status }: ${ item.title }` ).join( '\n' )
        notify( formattedMessage, "error", displayMessageTime )
    }
    else
    {
        const formattedMessage: string = `${ message.error.status }: ${ message.error.title }`
        notify( formattedMessage, "error", displayMessageTime )
    }
}


export function displaySuccessMessage( message: string )
{
    notify( message, "success", displayMessageTime )
}