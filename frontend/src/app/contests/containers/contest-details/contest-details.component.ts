import { Component, OnDestroy } from '@angular/core'
import { ActivatedRoute } from '@angular/router'
import { Subscription } from 'rxjs'


@Component( {
    selector: 'app-contest-details',
    templateUrl: './contest-details.component.html',
    styleUrls: [ './contest-details.component.scss' ]
} )
export class ContestDetailsComponent implements OnDestroy
{
    contestId!: number
    private subscription: Subscription

    constructor( private activateRoute: ActivatedRoute )
    {
        this.subscription = activateRoute.params.subscribe( params => this.contestId = params[ 'id' ] )
    }

    ngOnDestroy(): void
    {
        this.subscription?.unsubscribe()
    }
}