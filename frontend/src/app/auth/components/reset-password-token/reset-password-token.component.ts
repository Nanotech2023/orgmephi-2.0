import { Component } from '@angular/core'
import { Observable, of } from 'rxjs'
import { ActivatedRoute, Router } from '@angular/router'
import { catchError, filter, map, tap } from 'rxjs/operators'
import { UsersService } from '@api/users/users.service'
import { ResetPasswordUser } from '@api/users/models'
import { displayErrorMessage, displaySuccessMessage } from '@/shared/logging'


@Component( {
    selector: 'app-reset-password-token',
    templateUrl: './reset-password-token.component.html',
    styleUrls: [ './reset-password-token.component.scss' ]
} )
export class ResetPasswordTokenComponent
{
    token$!: Observable<string>
    newPasswordConfirmValue: string = ""
    newPasswordValue: string = ""

    constructor( private usersService: UsersService, private route: ActivatedRoute, private router: Router ) { }

    ngOnInit(): void
    {
        this.token$ = this.route.queryParams.pipe(
            filter( params => params.token ),
            map( params => params.token ),
            tap( ( token: string ) => { this.usersService.userRegistrationConfirmTokenPost( token ) } )
        )
    }

    onSubmit( token: string ): void
    {
        const resetPasswordUser: ResetPasswordUser = { password: this.newPasswordValue }
        this.usersService.userRegistrationRecoverTokenPost( token, resetPasswordUser ).pipe(
            tap( () => of( displaySuccessMessage( "Пароль успешно изменён" ) ) ),
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ),
            tap( () => this.router.navigate( [ '/login' ] ) )
        ).subscribe()
    }
}
