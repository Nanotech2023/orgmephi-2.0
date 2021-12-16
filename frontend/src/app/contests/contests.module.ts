import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { ContestsStore } from '@/contests/contests.store'
import { AgGridModule } from 'ag-grid-angular'
import { RouterModule } from '@angular/router'
import { CONTEST_ROUTES, CONTESTS_COMPONENTS } from '@/contests/contests.module.components'


@NgModule( {
    declarations: CONTESTS_COMPONENTS,
    imports: [
        SharedModule,
        AgGridModule,
        RouterModule.forChild( CONTEST_ROUTES )
    ],
    providers: [
        { provide: ContestsStore }
    ]
} )
export class ContestsModule {}