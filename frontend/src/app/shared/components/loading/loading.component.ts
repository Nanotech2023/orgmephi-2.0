import { Component, OnDestroy, OnInit } from '@angular/core'
import { LoadingService } from '@/shared/loading.service'
import { Subscription } from 'rxjs'


@Component( {
    selector: 'app-loading',
    templateUrl: './loading.component.html',
    styleUrls: [ './loading.component.scss' ]
} )
export class LoadingComponent implements OnInit, OnDestroy
{
    private subscription!: Subscription
    loading: boolean = false

    constructor( private loaderService: LoadingService )
    {
    }

    ngOnInit(): void
    {
        this.subscription = this.loaderService.isLoading.subscribe( ( item: boolean ) => this.loading = item )
    }

    ngOnDestroy(): void
    {
        this.subscription?.unsubscribe()
    }
}
