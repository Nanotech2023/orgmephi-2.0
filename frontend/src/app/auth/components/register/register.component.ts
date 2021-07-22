import { Component } from '@angular/core'
import { RegisterType, RegisterTypeEnum, RegisterTypes, UserRegister, validateUser, Agreements } from '@/auth/models'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'
import { Observable } from 'rxjs'
import { AuthService } from '@/auth/services/auth.service'


@Component( {
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: [ './register.component.scss' ]
} )
export class RegisterComponent
{
    agreements: string[] = Agreements
    registerTypes: RegisterType[] = RegisterTypes

    registerAttempt: UserRegister
    isRegistered$: Observable<boolean>

    selectedRegisterType: RegisterType | null
    hasRegisterNumber: boolean
    agreementAccepted: boolean

    constructor( private readonly store: Store<AuthState.State>, private readonly service: AuthService )
    {
        this.registerAttempt = this.service.createEmptyUser()
        this.isRegistered$ = this.store.select( AuthSelectors.selectIsRegistered )
        this.agreementAccepted = false
        this.selectedRegisterType = null
        this.hasRegisterNumber = false
    }

    selectRegisterType( registerType: RegisterType ): void
    {
        this.selectedRegisterType = registerType
    }

    isAvailable(): boolean
    {
        return this.selectedRegisterType !== null && this.selectedRegisterType?.value == RegisterTypeEnum.schoolOlymp
    }

    isValid( registerUser: UserRegister ): boolean
    {
        return validateUser( registerUser ) && this.agreementAccepted
    }

    register( registerUser: UserRegister ): void
    {
        this.store.dispatch( AuthActions.registerAttempt( { registration: registerUser } ) )
    }
}
