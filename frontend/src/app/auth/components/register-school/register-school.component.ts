import { Component, forwardRef, OnInit } from '@angular/core'
import { SchoolRegistrationRequestUser } from '@api/users/models'
import { AuthActions, AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'
import { NG_VALIDATORS } from '@angular/forms'
import { PasswordValidatorDirective } from '@/shared/password-validator.directive'
import { UsersService } from '@api/users/users.service'
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { Subscription } from 'rxjs'


export interface SchoolRegistrationRequestUserAttempt extends SchoolRegistrationRequestUser
{
    passwordConfirm: string
}


@Component( {
    selector: 'app-register-school',
    templateUrl: './register-school.component.html',
    styleUrls: [ './register-school.component.scss' ],
    providers: [
        { provide: NG_VALIDATORS, useExisting: forwardRef( () => PasswordValidatorDirective ), multi: true }
    ]
} )
export class RegisterSchoolComponent implements OnInit
{
    registerAttempt: SchoolRegistrationRequestUserAttempt
    hasRegisterNumber!: boolean
    agreementAccepted: boolean
    captchaUrl!: SafeUrl
    subscription!: Subscription

    constructor( private readonly usersService: UsersService, private readonly store: Store<AuthState.State>, private sanitizer: DomSanitizer )
    {
        this.registerAttempt = {
            auth_info: { email: '', password: '' },
            register_type: SchoolRegistrationRequestUser.RegisterTypeEnum.School,
            personal_info: { first_name: '', second_name: '', middle_name: '', date_of_birth: '' },
            passwordConfirm: ''
        }
        this.agreementAccepted = false
    }

    ngOnInit(): void
    {
        this.refreshToken()
    }

    isValid(): boolean
    {
        return this.agreementAccepted
    }

    register( registerUser: SchoolRegistrationRequestUser ): void
    {
        this.store.dispatch( AuthActions.registerRequest( { registrationRequestUser: registerUser } ) )
    }

    refreshToken(): void
    {
        this.usersService.userRegistrationCaptchaGet().subscribe( data =>
        {
            const unsafeImageUrl = URL.createObjectURL( data )
            this.captchaUrl = this.sanitizer.bypassSecurityTrustUrl( unsafeImageUrl )
        } )
    }
}
