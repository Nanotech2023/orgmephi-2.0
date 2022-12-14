import { Component, OnDestroy, OnInit } from '@angular/core'
import { Observable, of, Subscription } from 'rxjs'
import { UsersService } from '@api/users/users.service'
import { ActivatedRoute } from '@angular/router'
import { catchError, filter, map, tap } from 'rxjs/operators'
import { displayErrorMessage } from '@/shared/logging'


@Component( {
    selector: 'app-confirm-account-request-success',
    templateUrl: './confirm-account-request-success.component.html',
    styleUrls: [ './confirm-account-request-success.component.scss' ]
} )
export class ConfirmAccountRequestSuccessComponent implements OnInit, OnDestroy
{
    token!: string
    subscription!: Subscription

    constructor( private usersService: UsersService, private route: ActivatedRoute )
    {
    }

    ngOnInit()
    {
        this.subscription = this.route.queryParams.pipe(
            filter( params => params.token ),
            map( params => params.token ),
            tap( ( token: string ) =>
            {
                this.token = token
                this.usersService.userRegistrationConfirmTokenPost( token ).pipe( catchError( ( error: any ) => of( displayErrorMessage( error ) ) ) ).subscribe()
            } )
        ).subscribe()
    }

    ngOnDestroy(): void
    {
        this.subscription.unsubscribe()
    }
}
