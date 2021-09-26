import { NgModule } from '@angular/core'
import { ManageContestsComponent } from '@/manage-contests/containers/manage-contests/manage-contests.component'
import { SharedModule } from '@/shared/shared.module'
import { AgGridModule } from 'ag-grid-angular'
import { ManageContestsRoutingModule } from '@/manage-contests/manage-contests.routing.module'
import { AddContestModalComponent } from '@/manage-contests/components/add-contest-modal/add-contest-modal.component'


const COMPONENTS = [
    ManageContestsComponent,
    AddContestModalComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        AgGridModule,
        ManageContestsRoutingModule
    ]
} )
export class ManageContestsModule {}