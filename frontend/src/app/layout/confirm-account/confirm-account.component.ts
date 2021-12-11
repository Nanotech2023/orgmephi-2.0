import { Component } from '@angular/core'
import { UsersService } from '@api/users/users.service'


@Component( {
    selector: 'app-confirm-account',
    templateUrl: './confirm-account.component.html',
    styleUrls: [ './confirm-account.component.scss' ]
} )
export class ConfirmAccountComponent
{
    constructor( private usersService: UsersService )
    {
    }

    resendConfirmation()
    {
        this.usersService.userRegistrationResendPost()
    }
}