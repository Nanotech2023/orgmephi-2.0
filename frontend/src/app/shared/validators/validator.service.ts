import { Injectable } from '@angular/core'
import { ValidationErrors } from '@angular/forms'


@Injectable( {
    providedIn: 'root'
} )
export class ValidatorService
{
    validatePhoneNumber( phone: string ): ValidationErrors | null
    {
        const pattern = new RegExp( "^([+]?\\d[-.\\s]??)?(\\d{2,3}[-.\\s]??\\d{2,3}[-.\\s]??\\d{2}[-.\\s]??\\d{2}|\\(\\d{3}\\)[-.\\s]??\\d{3}[-.\\s]??\\d{2}[-.\\s]??\\d{2}|\\d{3}[-.\\s]??\\d{2}[-.\\s]??\\d{2})$" )
        if ( pattern.test( phone ) )
            return null
        else
            return ( { phoneNumberValid: false } )
    }

    validateEmail( email: string ): ValidationErrors | null
    {
        const pattern = new RegExp( "^([-!#$%&'*+\\/=?^`{}|~\\w]+(\\.[-!#$%&'*+\\/=?^`{}|~\\w]+)*|^\"([\\001-\\010\\013\\014\\016-\\037!#-\\[\\]-\\177]|\\\\[\\001-\\011\\013\\014\\016-\\177])*\")@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,})$|\\[(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)(\\.(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)){3}\\]$" )
        if ( pattern.test( email ) )
            return null
        else
            return ( { emailValid: false } )
    }

    validatePassword( password: string ): ValidationErrors | null
    {
        let value = password
        if ( !value )
        {
            return null
        }

        let upperCaseCharacters = /[A-Z]+/g
        if ( !upperCaseCharacters.test( value ) )
        {
            return { passwordStrength: `text has to contine Upper case characters,current value ${ value }` }
        }

        let lowerCaseCharacters = /[a-z]+/g
        if ( !lowerCaseCharacters.test( value ) )
        {
            return { passwordStrength: `text has to contine lower case characters,current value ${ value }` }
        }


        let numberCharacters = /[0-9]+/g
        if ( !numberCharacters.test( value ) )
        {
            return { passwordStrength: `text has to contine number characters,current value ${ value }` }
        }

        return null
    }
}