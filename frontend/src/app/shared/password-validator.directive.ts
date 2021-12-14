import { Directive } from '@angular/core'
import { Validator, AbstractControl, ValidationErrors, NG_VALIDATORS } from '@angular/forms'
import { ValidatorService } from '@/shared/validator.service'


@Directive( {
    selector: '[appPasswordValidator]',
    providers: [ { provide: NG_VALIDATORS, useExisting: PasswordValidatorDirective, multi: true } ]
} )
export class PasswordValidatorDirective implements Validator
{
    constructor( private validateService: ValidatorService ) {}

    validate( control: AbstractControl ): ValidationErrors | null
    {
        return this.validateService.validatePassword( control.value )
    }
}