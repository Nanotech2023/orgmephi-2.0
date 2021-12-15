import { Component } from '@angular/core'
import { UsersService } from '@api/users/users.service'


@Component( {
    selector: 'app-header-confirm-account',
    templateUrl: './header-confirm-account.component.html',
    styleUrls: [ './header-confirm-account.component.scss' ]
} )
export class HeaderConfirmAccountComponent
{
    constructor( private usersService: UsersService )
    {
    }

    resendConfirmation()
    {
        this.usersService.userRegistrationResendPost()
    }
}