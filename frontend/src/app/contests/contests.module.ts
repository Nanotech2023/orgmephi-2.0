import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { ContestsRoutingModule } from '@/contests/contests.routing.module'
import { ContestListComponent } from '@/contests/containers/contest-list/contest-list.component'
import { ContestDetailsComponent } from '@/contests/containers/contest-details/contest-details.component'
import { ContestsStore } from '@/contests/contests.store'
import { ContestListItemComponent } from '@/contests/containers/contest-list-item/contest-list-item.component'
import { ContestRegistrationComponent } from '@/contests/containers/contest-registration/contest-registration.component'
import { ContestAssignmentComponent } from '@/contests/containers/contest-assignment/contest-assignment.component'


const COMPONENTS = [
    ContestListComponent,
    ContestDetailsComponent,
    ContestListItemComponent,
    ContestRegistrationComponent,
    ContestAssignmentComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        ContestsRoutingModule
    ],
    providers: [
        { provide: ContestsStore }
    ]
} )
export class ContestsModule {}