import { Directive } from '@angular/core'
import { Validator, AbstractControl, ValidationErrors, NG_VALIDATORS } from '@angular/forms'
import { ValidatorService } from '@/shared/validator.service'


@Directive( {
    selector: '[appPhoneValidator]',
    providers: [ { provide: NG_VALIDATORS, useExisting: PhoneValidatorDirective, multi: true } ]
} )
export class PhoneValidatorDirective implements Validator
{
    constructor( private validateService: ValidatorService ) {}

    validate( control: AbstractControl ): ValidationErrors | null
    {
        return this.validateService.validatePhoneNumber( control.value )
    }
}