import { Component } from '@angular/core'
import { RegisterType, RegisterTypeEnum, RegisterTypes, UserRegister, validateUser, Agreements } from '@/auth/models'
import { AuthService } from '@/auth/services/auth.service'
import { RegisterResult } from '@/auth/models/registerResult'


@Component( {
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: [ './register.component.scss' ]
} )
export class RegisterComponent
{
    agreements: string[] = Agreements
    registerTypes: RegisterType[] = RegisterTypes

    registerUser: UserRegister
    selectedRegisterType: RegisterType | null
    hasRegisterNumber: boolean
    agreementAccepted: boolean
    registerResult: RegisterResult | null
    registrationCompleted: boolean

    constructor( private service: AuthService )
    {
        this.registerUser = service.createEmptyUser()
        this.agreementAccepted = false
        this.selectedRegisterType = null
        this.hasRegisterNumber = false
        this.registerResult = null
        this.registrationCompleted = false
    }

    selectRegisterType( registerType: RegisterType ): void
    {
        this.selectedRegisterType = registerType
    }

    isAvailable(): boolean
    {
        return this.selectedRegisterType !== null && this.selectedRegisterType?.value == RegisterTypeEnum.schoolOlymp
    }

    isValid(): boolean
    {
        return validateUser( this.registerUser ) && this.agreementAccepted
    }

    register(): void
    {
        this.registerResult = this.service.register( this.registerUser )
        this.registrationCompleted = true
    }
}
