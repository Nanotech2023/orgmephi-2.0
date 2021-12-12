import notify from 'devextreme/ui/notify'
import { ErrorMessage } from '@/shared/logging'


const displayMessageTime = 3000


export function displayErrorMessage( message: ErrorMessage ): void
{
    const formattedMessage: string = message.error.errors.map( item => `${ item.status }: ${ item.title }` ).join( '\n' )
    notify( formattedMessage, "error", displayMessageTime )
}


export function displaySuccessMessage( message: string )
{
    notify( message, "success", displayMessageTime )
}